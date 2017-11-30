----------------------------------------------------------------

AP_CFG = {}

AP_CFG.ssid = "RFLOCUS"

AP_CFG.pwd = "oficina0"

AP_CFG.auth = AUTH_OPEN

AP_CFG.channel = 1

AP_CFG.hidden = false

AP_CFG.max = 3

AP_CFG.beacon = 100

AP_CFG.save = false

----------------------------------------------------------------

AP_IP_CFG = {}

AP_IP_CFG.ip = "192.168.100.1"

AP_IP_CFG.netmask = "255.255.255.0"

AP_IP_CFG.gateway = "192.168.100.1"

----------------------------------------------------------------

AP_DHCP_CFG = {}

AP_DHCP_CFG.start = "192.168.100.2"

----------------------------------------------------------------

STA_CFG = {}

STA_CFG.ssid = "RFLocus"

--STA_CFG.ssid = "Natalia"

--STA_CFG.ssid = "Net-Virtua-7245"

STA_CFG.pwd = "oficina3"

--STA_CFG.pwd = "outubro10"

--STA_CFG.pwd = "6305372450"

STA_CFG.auto = true

STA_CFG.bssid = "B8-27-EB-A3-7D-75"

--STA_CFG.bssid = "90-17-AC-E7-3A-A0"

--STA_CFG.bssid = "6C-B5-6B-8B-4D-90"

STA_CFG.save = false

----------------------------------------------------------------

wifi.ap.config(AP_CFG)

wifi.ap.setip(AP_IP_CFG)

wifi.ap.dhcp.config(AP_DHCP_CFG)

wifi.ap.dhcp.start()

wifi.sta.config(STA_CFG)

----------------------------------------------------------------

wifi.setmode(wifi.STATIONAP)

wifi.setphymode(wifi.PHYMODE_B)

----------------------------------------------------------------

MEASUREMENTS = {}

MEASUREMENTS.type = "ctrl"

MEASUREMENTS.data = {}

----------------------------------------------------------------

tmr.unregister(1)

tmr.alarm(1, 15000, tmr.ALARM_AUTO, function()

        for key, value in pairs(MEASUREMENTS.data) do

            MEASUREMENTS.data[key].time = tmr.time() - MEASUREMENTS.data[key].time

        end

        ok, json = pcall(sjson.encode, MEASUREMENTS)

        if ok then

            print(json)

        else

            print("JSON encoding failed")

        end

        http.put('http://192.168.0.1:5500/',

                 'Content-Type: application/json\r\n',

                 json,

                 function(code, data)

                     if (code < 0) then

                         print("HTTP request failed")

                     else

                         print(code, data)

                     end

                 end)

        MEASUREMENTS.data = {}

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.WIFI_MODE_CHANGED)

wifi.eventmon.register(wifi.eventmon.WIFI_MODE_CHANGED, function(T)

    print("\n\tSTA_WIFI_MODE_CHANGED" .. "\n\t\told_mode: " .. T.old_mode .. "\n\t\tnew_mode: " .. T.new_mode)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.STA_CONNECTED)

wifi.eventmon.register(wifi.eventmon.STA_CONNECTED, function(T)

    print("\n\tSTA_CONNECTED" .. "\n\t\tSSID: " .. T.SSID .. "\n\t\tBSSID: " .. T.BSSID .. "\n\t\tchannel: " .. T.channel)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.STA_DISCONNECTED)

wifi.eventmon.register(wifi.eventmon.STA_DISCONNECTED, function(T)

    print("\n\tSTA_DISCONNECTED" .. "\n\t\tSSID: " .. T.SSID .."\n\t\tBSSID: " .. T.BSSID .. "\n\t\treason: " .. T.reason)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.STA_AUTHMODE_CHANGE)

wifi.eventmon.register(wifi.eventmon.STA_AUTHMODE_CHANGE, function(T)

    print("\n\tSTA_AUTHMODE_CHANGE" .. "\n\t\told_auth_mode: " .. T.old_auth_mode .. "\n\t\tnew_auth_mode: " .. T.new_auth_mode)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.STA_GOT_IP)

wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, function(T)

    print("\n\tSTA_GOT_IP" .. "\n\t\tIP: " .. T.IP .. "\n\t\tnetmask: " .. T.netmask .. "\n\t\tgateway: " .. T.gateway)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.STA_DHCP_TIMEOUT)

wifi.eventmon.register(wifi.eventmon.STA_DHCP_TIMEOUT, function()

    print("\n\tSTA_DHCP_TIMEOUT")

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.AP_STACONNECTED)

wifi.eventmon.register(wifi.eventmon.AP_STACONNECTED, function(T)

    print("\n\tAP_STACONNECTED" .. "\n\t\tMAC: " .. T.MAC .. "\n\t\tAID: " .. T.AID)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.AP_STADISCONNECTED)

wifi.eventmon.register(wifi.eventmon.AP_STADISCONNECTED, function(T)

    print("\n\tAP_STADISCONNECTED" .. "\n\t\tMAC: " .. T.MAC .. "\n\t\tAID: " .. T.AID)

end)

----------------------------------------------------------------

wifi.eventmon.unregister(wifi.eventmon.AP_PROBEREQRECVED)

wifi.eventmon.register(wifi.eventmon.AP_PROBEREQRECVED, function(T)

    if (T.MAC == "1c:56:fe:a0:68:a8") then

        print("\n\tAP_PROBEREQRECVED" .. "\n\t\tMAC: " .. T.MAC .. "\n\t\tRSSI: " .. T.RSSI)

        MEASUREMENT = {}

        MEASUREMENT.time = tmr.time()

        MEASUREMENT.rfid = wifi.sta.getmac()

        MEASUREMENT.apid = T.MAC

        MEASUREMENT.rssi = T.RSSI

        MEASUREMENTS.data[#MEASUREMENTS.data + 1] = MEASUREMENT

    end

end)

----------------------------------------------------------------

