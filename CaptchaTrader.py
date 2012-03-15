# -*- coding: UTF-8 -*-
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: Jose Sanchez <jose@serhost.com> (c) 2012
    @version: 0.1
"""
import json
import urllib2
import urllib

class CaptchaTrader():

    __SUBMIT_URL__ = "http://captchatrader.com/api/submit"
    __RESPOND_URL__ = "http://captchatrader.com/api/respond"
    __GET_CREDITS_URL__ = "http://captchatrader.com/api/get_credits/username:%(user)s/password:%(password)s/"

    def __init__(self, user, password, api_key):
        self.user=user
        self.password=password
        self.api_key=api_key

    def getCredits(self):
        try:
            response=urllib2.urlopen(CaptchaTrader.__GET_CREDITS_URL__ % {"user": self.user, "password": self.password})
            credits=json.loads(response.read())
        except:
            raise Exception("-1", "Unexpected exception. Username/password incorrect?")

        if (credits[0] != 0):
            raise Exception("-1", credits[1])
        else:
            return int(credits[1])

    def respond(self, ticket, is_correct):
        data = urllib.urlencode({
            'username': self.user,
            'password': self.password,
            'ticket': ticket,
            'is_correct': is_correct
        })

        try:
            req=urllib2.Request(self.__RESPOND_URL__, data)
            res=urllib2.urlopen(req)
            response=json.loads(res.read())
        except:
            raise Exception("-1", "Unexpected exception. Username/password incorrect? Ticket incorrect or used?")

        if (response[0] != 0):
            raise Exception("-1", response[1])
        else:
            return int(response[0])

    def submitFilePath(self, filepath):
        return self.submit(open(filepath, "rb").read().encode("base64"))

    def submitURL(self, url):
        r=urllib2.urlopen(url)
        return self.submit(r.read().encode("base64"))

    def submit(self, captchabase64):
        data = urllib.urlencode({
            'api_key': self.api_key,
            'password': self.password,
            'username': self.user,
            'value': captchabase64
        })

        try:
            req=urllib2.Request(self.__SUBMIT_URL__, data)
            res=urllib2.urlopen(req)
            response=json.loads(res.read())
        except:
            print response
            print res.read()
            raise Exception("-1", "Unexpected exception. Username/password incorrect? Image format incorrect?")

        return response

#Example of use:
#a = CaptchaTrader("Username", "Password", "API_KEY")
#print a.getCredits()
#response = a.submitURL("http://www.google.com/images/srpr/logo3w.png")
#response = a.submitFilePath("/tmp/filetest.png")
#response = a.submit(open("/tmp/filetest.png", "rb").read().encode("base64"))
#print "Ticket: ", response[0]
#print "CAPTCHA: ", response[1]
#a.respond(response[0],True);
