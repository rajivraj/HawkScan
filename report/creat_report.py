from datetime import datetime
import csv

def create_report(directory, cookie_):
    """
    Create_report: make a html report with url, waf, email...
    """
    urls = ""
    waf = ""
    mails = ""
    nowdate = datetime.now()
    nowdate = "{}-{}-{}".format(nowdate.day, nowdate.month, nowdate.year)
    #directory = "../" + directory
    if cookie_:
        auth_stat = "Authenticated"
    else:
        auth_stat = "No Authenticated"
    with open("report/report_"+ directory.split("/")[-1] + ".html", "a+") as test:
        with open(directory + "/scan.txt", "r") as scan:
            for s in scan.read().splitlines():
                s = s.split(" ")
                s0 = s[0]
                s1 = s[1]
                if s0 == "[+]":
                    if "301" in s or "302" in s:
                        if s[2] == "301":
                            s0 = s0.replace("[+]", "301")
                        elif s[2] == "302":
                            s0 = s0.replace("[+]", "302")
                        urls += """
                            <tr>
                            <td style="color: orange; ">{}</td>
                            <td style="color: orange; "><a href="{}" target="_blank" style="color: white;">{}</a></td>
                            <td style="color: orange; ">{}</td>
                            </tr>
                            """.format(nowdate, s1, s1, s0)
                    else:
                        s0 = s0.replace("[+]", "200")
                        urls += """
                        <tr>
                        <td style="color: green; ">{}</td>
                        <td style="color: green; "><a href="{}" target="_blank" style="color: white;">{}</td>
                        <td style="color: green; ">{}</td>
                        </tr>
                        """.format(nowdate, s1, s1, s0)
                elif s0 == "[x]":
                    s0 = s0.replace("[x]", "403")
                    urls += """
                        <tr>
                        <td style="color: red; ">{}</td>
                        <td style="color: red; "><a href="{}" target="_blank" style="color: white;">{}</a></td>
                        <td style="color: red; ">{}</td>
                        </tr>
                        """.format(nowdate, s1, s1, s0)
                elif s0 == "[-]":
                    if "401" in s:
                        if s[2] == "401":
                            s0 = s0.replace("[-]","401")
                        urls += """
                            <tr>
                            <td style="color: orange; ">{}</td>
                            <td style="color: orange; "><a href="{}" target="_blank" style="color: white;">{}</a></td>
                            <td style="color: orange; ">{}</td>
                            </tr>
                            """.format(nowdate, s1, s1, s0)
                elif s0 == "[!]":
                    if "400" in s:
                        if s[2] == "400":
                            s0 = s0.replace("[!]","400")
                        urls += """
                            <tr>
                            <td style="color: red; ">{}</td>
                            <td style="color: red; "><a href="{}" target="_blank" style="color: white;">{}</a></td>
                            <td style="color: red; ">{}</td>
                            </tr>
                            """.format(nowdate, s1, s1, s0)
        try:
            with open(directory + "/waf.txt", "r") as waff:
                waf_res = ""
                for w in waff.read().splitlines():
                    if "The site" in w:
                        waf_res = w
                if waf_res:
                    waf += """
                        <span class="subText" style='color: red;'>{}</span>
                    """.format(waf_res)
        except:
            waf += """
                <span class="subText" style='color: green;'>This site dosn't seem to use a WAF</span>
            """
        try:
            with open(directory + "/mail.csv", "r") as csvFile:
                reader = csv.reader(csvFile)
                for row in reader:
                    mail = row[0]
                    stat = row[1]
                    if "no" in stat:
                        mails += """
                            <tr>
                            <td style="color: green; ">{}</td>
                            <td style="color: green; ">{}</td>
                            </tr>
                            """.format(mail, stat)
                    else:
                        mails += """
                            <tr>
                            <td style="color: red; ">{}</td>
                            <td style="color: red; ">{}</td>
                            </tr>
                            """.format(mail, stat)
        except:
            mails = "<tr><td><b> No emails found </b></td></tr>"
        try:
            link = ""
            with open(directory + "/links.txt", "r") as links:
                for l in links.read().splitlines():
                    link += """
                        <tr>
                        <td><a href="{}" target="_blank" style="color: white;">{}</a></td>
                        </tr>
                        """.format(l, l)
        except:
            link = "<tr><td> No links found </td></tr>"
        try:
            wayback = ""
            with open(directory + "/wayback.txt", "r") as waybacks:
                for wb in waybacks.read().splitlines():
                    w = wb.split(",")
                    w_status = w[1]
                    wayback += """
                        <tr>
                        <td><a href="{}">{}</a></td>
                        <td>{}</td>
                        </tr>
                        """.format(w[0], w[0], w_status)
        except:
            wayback = "<tr><td><b> No wayback found </b></td></tr>"
        try:
            with open(directory + "/cms.txt","r") as cmsFile:
                cms = ""
                for cms_read in cmsFile.read().splitlines():
                    cms += """
                        <span class='subText' color: green; ">{}</span>
                        """.format(cms_read)
        except:
            cms = "<span class='subText' style='color: red;'> This site dosn't seem to use a CMS </span>"
        test.write('''
            <!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Hawkscan Report</title>
        <link href="charte.css" rel="stylesheet">
        <link href="page.css" rel="stylesheet">
    </head>

    <body>
        
        <header class="title w100">
            <div class="container">
                <h1>Hawkscan Report</h1>
            </div>
        </header>

        <main>
            <div class="subTitle container">
                <div class="w100 flex flex-jsb">
                    <div class="w1-3 centerText flex flex-dc flex-aic flex-jcc">
                        <h2>WAF</h2>
                        {}
                    </div>
                    <div class="w1-3 centerText flex flex-dc flex-aic flex-jcc">
                        <h2>CMS</h2>
                        {}
                    </div>
                    <div class="w1-3 centerText flex flex-dc flex-aic flex-jcc">
                        <h2>Status</h2>
                        <span class="subText">{}</span>
                    </div>
                </div>
            </div>
            <div class="subLinkSection w100">
                <div class="subLinkBloc w100">
                    <input type="radio" id="s1" name="s" checked/>
                    <input type="radio" id="s2" name="s"/>
                    <input type="radio" id="s3" name="s"/>
                    <input type="radio" id="s4" name="s"/>
                    <div class="subLink">
                        <div class="tabs container flex flex-jsb">
                            <label class="w1-4 centerText" for="s1">URLs</label>
                            <label class="w1-4 centerText" for="s2">Mails</label>
                            <label class="w1-4 centerText" for="s3">Links</label>
                            <label class="w1-4 centerText" for="s4">Wayback</label>
                        </div>
                    </div>
                    <ul class="sections container">
                    <center>
                        <li class="d-flex flex-dc">
                            <h3>URLs</h3>
                            <div class="tableau">
                                <table>
                                    <tr>
                                      <td>Date</td>
                                      <td>Url</td>
                                      <td>Status</td>
                                        {}
                                    </tr>
                                  </table>
                            </div>
                        </li>
                        <li class="d-flex flex-dc">
                            <h3>MAIL</h3>
                            <div class="tableau">
                                <table>
                                    <tr>
                                      <td>Mails</td>
                                      <td>Status</td>
                                        {}
                                    </tr>
                                  </table>
                            </div>
                        </li>
                        <li class="d-flex flex-dc">
                            <h3>Links</h3>
                            <div class="tableau">
                                <table>
                                    <tr>
                                      {}
                                    </tr>
                                  </table>
                            </div>
                        </li>
                        <li class="d-flex flex-dc">
                            <h3>Wayback</h3>
                            <div class="tableau">
                                <table>
                                    <tr>
                                      {}
                                    </tr>
                                  </table>
                            </div>
                        </li>
                    </center>
                    </ul>
                </div>

                <!-- <div class="w1-4 centerText">
                    <h2>Test Subtitle</h2>
                </div>
                <div class="w1-4 centerText">
                    <h2>Test Subtitle</h2>
                </div>
                <div class="w1-4 centerText">
                    <h2>Test Subtitle</h2>
                </div>
                <div class="w1-4 centerText">
                    <h2>Test Subtitle</h2>
                </div> -->
            </div>
        </main>

        
    </body>
</html>'''.format(waf, cms, auth_stat, urls, mails, link, wayback))

"""if __name__ == '__main__':
    directory = "../sites/fr.chaturbate.com"
    cookie_ = None
    create_report(directory, cookie_)"""