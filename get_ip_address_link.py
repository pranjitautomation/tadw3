
import imaplib
import email
import re

user = 'ta@baylifept.com'
password = 'BAY1234!'
imap_url = 'outlook.office365.com'
senderemail = "revflow-noreply@webpt.com"


def get_ip_address_verification_link():
    """
    This method is used to get the ip address authentication link
    from the outlook mail
    """

    def mult_byte_to_single_byte(p):
        s = p.decode('utf-8')
        btcode = s.split(" ")
        codes = []
        for x in btcode:
            codes.append(x.encode())
        return codes

    def auth(user, password, imap_url):
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user, password)
        return con

    def search(key, value, con):
        result, data = con.search(None, key, '"{}"'.format(value))
        return data

    def login_and_get_latest_mail() -> bytes:
        """
        This method log in the mail and get the latest mail

        Returns:
            bytes : returns the latest mail
        """
        con = auth(user, password, imap_url)
        con.select('INBOX')

        total_number_of_emails = search("FROM", senderemail, con)[0]
        bytecodes = mult_byte_to_single_byte(total_number_of_emails)

        for x in bytecodes:
            result, data = con.fetch(x, '(RFC822)')
            raw = email.message_from_bytes(data[0][1])

        return raw

    def get_text(msg) -> str:
        """
        this method returns the body text of the mail

        Args:
            msg (bytes): msg is the latest mail in bytes

        Returns:
            str: returns the mail's body text
        """
        if msg.is_multipart():
            return get_text(msg.get_payload(0))
        else:
            return msg.get_payload(None, True).decode("utf-8")

    def get_authentication_link() -> str:
        """
        This method is used to get authentication link from the mail

        Returns:
            _string: returns the link to verify ip address
        """
        raw = login_and_get_latest_mail()
        ans = get_text(raw)
        link = re.search("<br><br>(.+?)<br><br>", ans).group(1)
        print(link)
        return link

    get_authentication_link()
