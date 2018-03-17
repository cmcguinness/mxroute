import requests
from requests.auth import HTTPBasicAuth
import json
import urllib.parse

class MXroute:
    """
        This is a small set of functions to demonstrate API access to MXroute's cpanel implementation

        The goal is to demonstrate a more convient (or automated) means of adding and removing
        email accounts and email forwarders.  This is neither comprehensive nor bullet-proof.

        This code has some python 3 only quirks (just urllib.parse?), so would need to be lightly
        refactored for python 2.

        Definition of functions called is given here:
            https://documentation.cpanel.net/display/DD/UAPI+Modules+-+Email

    """

    def __init__(self, userid, password, server='eagle.mxlogin.com:2083'):
        """
            Instantiates the class, defines the login parameters
            
            Parameters:
                
            userid : string
            password  : string
                password for the account
            server : string (optional)
                server and port, defaults to the one I use :-)
                
        """
        self.userid = userid
        self.password = password
        self.server = server


    def make_call(self, function):
        """
            This is used to actually make the call to the server

            function: string
                The "function" to be performed, but is basically everything after the domain:port in the URL

            return:
                parsed JSON of the response, or None if there's an error.
                self.last_status_code contains the HTTP status for further inspection
                self.last_response contains the last full response objecto
        """

        response = requests.get('https://' + self.server + '/' + function, auth=HTTPBasicAuth(self.userid, self.password))
        self.last_status_code = response.status_code
        self.last_response = response
        if response.status_code != 200:
            return None
        return json.loads(response.content)

    #
    #   Domain Info Calls
    #
    def list_domains(self):
        """
            Return a list of all domains and subdomains managed by the account
        """
        r = self.make_call('execute/DomainInfo/list_domains')
        if r is None:
            return None
        return r['data']

    def single_domain_data(self, domain):
        """
            Return information about a specific domain managed by the account

            domain: string
                The domain, eg fooobar.com

            returns:
                Whatever we get back or None if there's an error
        """
        r = self.make_call('/execute/DomainInfo/single_domain_data?domain='+domain)
        if r is None:
            return None
        return r['data']


    #
    #   Email Acocount Domain Information
    #
    def list_mail_domains(self):
        """
            List all domains that are being used for email

            returns:
                An array of string holding domains, or None if error
        """
        r = self.make_call('execute/Email/list_mail_domains')
        if r is None:
            return None
        domains = []
        for d in r['data']:
            domains.append(d['domain'])
        return domains


    #
    #   Manage Email Forwarders
    #

    def add_forwarder(self, email_from, email_to):
        """
            Adds an email forwarder

            email_from: string
                The email account to forward from, in the form user@domain.tld
            email_to: string
                The email account to forward to, in the form user@domain.tld
            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        from_user, from_domain = email_from.split('@')
        r = self.make_call('/execute/Email/add_forwarder?domain={}&email={}&fwdopt=fwd&fwdemail={}'.format(from_domain, email_from, email_to))
        return r

    def list_forwarders(self, email_domain):
        """
            Returns a list of forwarded email accounts for a specific domain

            email_domain: string
                The domain we're interested in, e.g. foobar.com

            returns:
                dictionary holding email_from:email_to forwarding definitions
        """
        r = self.make_call('/execute/Email/list_forwarders?domain={}'.format(email_domain))
        if r is None:
            return None

        forwards = {}
        for d in r['data']:
            forwards[d['dest']] = d['forward']

        return forwards

    def delete_forwarder(self, email_from, email_to):
        """
            Deletes an existing email forwarding account

            email_from: string
                The account mail is being forwarded from, eg foo@bar.com
            email_to: string
                The account mail is being forwarded to, et bar@foo.com

            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        r = self.make_call('/execute/Email/delete_forwarder?address={}&forwarder={}'.format(email_from, email_to))
        return r



    #
    #   Manage Email Mailboxes (Not forwarders)
    #
    def add_pop(self, email_address, password, quota=0):
        """
            Add a new, fully hosted email account

            email_address: string
                The email address to host
            password: string
                The password for this email address
            quota: int, optional
                Quote, in MB, of the account.  Defaults to unlimited

            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        email_user, email_domain = email_address.split('@')
        password = urllib.parse.quote_plus(password)
        r = self.make_call('/execute/Email/add_pop?email={}&password={}&domain={}&quota={}'.format(email_user, password, email_domain, quota))
        return r


    def delete_pop(self, email_address):
        """
            Deletes an existing email account

            email_address: string
                The email address to delete

            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        email_user, email_domain = email_address.split('@')
        r = self.make_call('/execute/Email/delete_pop?email={}&domain={}'.format(email_user, email_domain))
        return r

    def change_pop_password(self, email_address, newpassword):
        """
            Changes the password on an existing email account

            email_address: string
                The email address to delete
            newpassword: string
                The new password to use

            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        email_user, email_domain = email_address.split('@')
        newpassword = urllib.parse.quote_plus(newpassword)
        r = self.make_call('/execute/Email/passwd_pop?email={}&password={}&domain={}'.format(email_user, newpassword, email_domain))
        return r

    def change_pop_quota(self, email_address, quota):
        """
            Changes the mailbox quota for an email address

            email_address: string
                The email address to host
            quota: int
                New quota, in MB, of the account.

            returns:
                Whatever cpanel hands us back, or None if an http error
        """
        email_user, email_domain = email_address.split('@')
        r = self.make_call('/execute/Email/edit_pop_quota?email={}&domain={}&quota={}'.format(email_user, email_domain, quota))
        return r
