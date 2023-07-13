import quickfix as fix

__SOH__ = chr(1)

def getValue(message, field):
    key = field
    message.getField(key)
    return key.getValue()

def getHeaderValue(message, field):
    key = field
    message.getHeader().getField(key)
    return key.getValue()

class Application(fix.Application):
    """FIX Application"""

    def __init__(self, target, sender, password, account):
        """
        ### Start Application
        
            - Start FIX Session    
        """
        
        super().__init__()
        
        self.senderCompID = sender
        self.targetCompID = target
        self.password = password
        self.account = account        
      
    def onCreate(self, session):
        """
        onCreate is called when quickfix creates a new session.
        A session comes into and remains in existence for the life of the application.
        Sessions exist whether or not a counter party is connected to it.
        As soon as a session is created, you can begin sending messages to it.
        If no one is logged on, the messages will be sent at the time a connection is established with the counterparty.
        """
       
        targetCompID = session.getTargetCompID().getValue()
        try:
            self.sessions[targetCompID] = {}
        except AttributeError:
            self.sessions               = {}
            self.sessions[targetCompID] = {}
            
        self.sessions[targetCompID]['session']   = session
        self.sessions[targetCompID]['connected'] = False
        self.sessions[targetCompID]['exchID']    = 0
        self.sessions[targetCompID]['execID']    = 0
        
    def onLogon(self, session):
        """
        onLogon notifies you when a valid logon has been established with a counter party.
        This is called when a connection has been established and the FIX logon process has completed with both parties exchanging valid logon messages.
        """

        targetCompID = session.getTargetCompID().getValue()
        self.sessions[targetCompID]['connected'] = True
                
    def onLogout(self, session):
        """
        onLogout notifies you when an FIX session is no longer online.
        This could happen during a normal logout exchange or because of a forced termination or a loss of network connection.
        """
        
        targetCompID = session.getTargetCompID().getValue()
        self.sessions[targetCompID]['connected'] = False
        

    def toAdmin(self, message, session):
        """
        toAdmin provides you with a peek at the administrative messages that are being sent from your FIX engine
        to the counter party. This is normally not useful for an application however it is provided for any logging
        you may wish to do. Notice that the FIX::Message is not const.
        This allows you to add fields to an adminstrative message before it is sent out.
        """

        if getHeaderValue(message, fix.MsgType()) == fix.MsgType_Logon:
            message.getHeader().setField(553, self.senderCompID)
            message.getHeader().setField(554, self.password)
        
    def fromAdmin(self, message, session):
        """
        fromAdmin notifies you when an administrative message is sent from a counterparty to your FIX engine. This can be usefull for doing extra validation on logon messages like validating passwords.
        Throwing a RejectLogon exception will disconnect the counterparty.
        """

        msg = message.toString().replace(__SOH__, "|")
        print("S fromAdmin>> (%s)" % msg)        
              
    def toApp(self, message, session):
        """
        toApp is a callback for application messages that are being sent to a counterparty.
        If you throw a DoNotSend exception in this function, the application will not send the message.
        This is mostly useful if the application has been asked to resend a message such as an order that is no longer relevant for the current market.
        Messages that are being resent are marked with the PossDupFlag in the header set to true;
        If a DoNotSend exception is thrown and the flag is set to true, a sequence reset will be sent in place of the message.
        If it is set to false, the message will simply not be sent. Notice that the FIX::Message is not const.
        This allows you to add fields to an application message before it is sent out.
        """
        
        msg = message.toString().replace(__SOH__, "|")
        print("S toApp>> (%s)" % msg)        
    
    def fromApp(self, message, session):
        """
        fromApp receives application level request.
        If your application is a sell-side OMS, this is where you will get your new order requests.
        If you were a buy side, you would get your execution reports here.
        If a FieldNotFound exception is thrown,
        the counterparty will receive a reject indicating a conditionally required field is missing.
        The Message class will throw this exception when trying to retrieve a missing field, so you will rarely need the throw this explicitly.
        You can also throw an UnsupportedMessageType exception.
        This will result in the counterparty getting a reject informing them your application cannot process those types of messages.
        An IncorrectTagValue can also be thrown if a field contains a value you do not support.
        """  

        msg = message.toString().replace(__SOH__, "|")
        print("S fromApp>> (%s)" % msg)              