local CONFIG = {
    salt = "secret_salt",
    xor_shift = 7,
    header = "GGL-sandbox",
    split_char = "|",
    execute_payload = true,     -- run payload if valid
    signal_expiry = true,       -- flip expired flag when time runs out
    validfor = 60,              -- seconds
    varexpiry = "myexpiry",     -- global var names
    varpayload = "mypayload",
    varexpired = "myexpired",
    varisexpired = "is_expired",
    noncefile = "used_nonces.txt", -- replay log filename
    payload_mode = "code",      -- "code" = run with loadstring, "url" = fetch and run
    show_timer = true,          -- update label with countdown
    error_prefix = "[KeySys] ", -- prepend to error messages
    max_payload_length = 2000   -- reject payloads longer than this
}

-- Load SHA-256 implementation from your repo
loadstring(game:HttpGet("https://raw.githubusercontent.com/g00glesucksdude-oss/Key-system-base/refs/heads/main/sha256"))()
-- Now sha256() is available globally

-- XOR deobfuscation using bit32.bxor
local function xor_deobfuscate(data, salt, shift)
    local result = {}
    for i = 1, #data do
        local key = bit32.bxor(string.byte(salt:sub((i - 1) % #salt + 1)), shift)
        result[i] = string.char(bit32.bxor(string.byte(data:sub(i, i)), key))
    end
    return table.concat(result)
end

-- Replay protection
local function nonce_used(nonce)
    local path = CONFIG.noncefile
    if not isfile or not readfile or not writefile then
        return false -- skip if file APIs not supported
    end
    if not isfile(path) then writefile(path, "") end
    local content = readfile(path) or ""
    for line in string.gmatch(content, "[^\r\n]+") do
        if line == nonce then return true end
    end
    return false
end

local function mark_nonce_used(nonce)
    if appendfile then
        appendfile(CONFIG.noncefile, nonce .. "\n")
    end
end

-- Load GUI (this builds the interface and fires KeyValidationEvent)
loadstring(game:HttpGet("https://raw.githubusercontent.com/g00glesucksdude-oss/Complicated-key-system/main/gui"))()

-- Grab the event the GUI fires when Validate is clicked
local event = game:GetService("CoreGui"):WaitForChild("KeyValidationEvent")

-- Grab the label so we can update it
local gui = game:GetService("Players").LocalPlayer.PlayerGui:WaitForChild("KeyValidatorGui")
local frame = gui:WaitForChild("Frame")
local outputLabel = frame:WaitForChild("TextLabel")

-- Hook validation logic to the event
event.Event:Connect(function(input)
    if not input or input == "" then
        outputLabel.Text = CONFIG.error_prefix .. "Enter a key"
        return
    end

    local decrypted = xor_deobfuscate(input, CONFIG.salt, CONFIG.xor_shift)
    local parts = string.split(decrypted, CONFIG.split_char)
    if #parts ~= 6 or parts[1] ~= CONFIG.header then
        outputLabel.Text = CONFIG.error_prefix .. "Invalid format"
        return
    end

    local validfor = tonumber(parts[2])
    local expiresat = tonumber(parts[3])
    local payload = parts[4]
    local nonce = parts[5]
    local digest = parts[6]

    if not validfor or not expiresat or not nonce or not digest then
        outputLabel.Text = CONFIG.error_prefix .. "Malformed key fields"
        return
    end

    if validfor ~= CONFIG.validfor then
        outputLabel.Text = CONFIG.error_prefix .. "Invalid validity window"
        return
    end

    -- Compute expected digest
    local concat = tostring(validfor)
        .. CONFIG.split_char .. tostring(expiresat)
        .. CONFIG.split_char .. payload
        .. CONFIG.split_char .. nonce
        .. CONFIG.split_char .. CONFIG.salt

    if type(sha256) ~= "function" then
        outputLabel.Text = CONFIG.error_prefix .. "SHA256 not loaded"
        return
    end

    local expected = sha256(concat)
    if (digest or ""):lower() ~= (expected or ""):lower() then
        outputLabel.Text = CONFIG.error_prefix .. "Digest mismatch"
        return
    end

    if nonce_used(nonce) then
        outputLabel.Text = CONFIG.error_prefix .. "Replay detected"
        return
    end
    mark_nonce_used(nonce)

    -- Inject globals
    getgenv()[CONFIG.varexpiry] = expiresat
    getgenv()[CONFIG.varpayload] = payload
    getgenv()[CONFIG.varexpired] = false
    getgenv()[CONFIG.varisexpired] = function()
        return os.time() >= getgenv()[CONFIG.varexpiry]
    end

    -- Countdown updater
    if CONFIG.show_timer then
        task.spawn(function()
            while true do
                task.wait(1)
                local left = getgenv()[CONFIG.varexpiry] - os.time()
                if left <= 0 then
                    getgenv()[CONFIG.varexpired] = true
                    outputLabel.Text = CONFIG.error_prefix .. "Key expired"
                    break
                else
                    outputLabel.Text = "Time left: " .. left .. "s"
                end
            end
        end)
    end

    -- Execute payload if valid
    if CONFIG.execute_payload and not getgenv()[CONFIG.varisexpired]() then
        if #getgenv()[CONFIG.varpayload] > CONFIG.max_payload_length then
            outputLabel.Text = CONFIG.error_prefix .. "Payload too long"
            return
        end
        local ok, err
        if CONFIG.payload_mode == "code" then
            ok, err = pcall(function()
                loadstring(getgenv()[CONFIG.varpayload])()
            end)
        elseif CONFIG.payload_mode == "url" then
            ok, err = pcall(function()
                local src = game:HttpGet(getgenv()[CONFIG.varpayload])
                loadstring(src)()
            end)
        end
        if not ok then
            outputLabel.Text = CONFIG.error_prefix .. "Payload error: " .. tostring(err)
        end
    end
end)
