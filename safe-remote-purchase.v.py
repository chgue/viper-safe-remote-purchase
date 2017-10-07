#Safe Remote Purchase (https://github.com/ethereum/solidity/blob/develop/docs/solidity-by-example.rst) ported to viper
#Value of the item
value: public(wei_value)
seller: public(address)
buyer: public(address)
state: num # 0 = created, 1 = locked, 2 = finished/inactive
#Seller initializes the purchase by depositing 2*value in the contract
@payable
def __init__():
    #Assert that the value is a multiple of 2
    assert (msg.value % 2) == 0
    self.value = msg.value / 2
    self.seller = msg.sender
    self.state = 0 #Created
def abort():
    assert self.state == 0 #Is the contract still refundable
    assert msg.sender == self.seller #Only seller can refund his deposit before any buyer purchases the item
    self.state = 2 #Possible unnecessary because of selfdestruct?
    selfdestruct(self.seller) #Refunds seller

@payable
def purchase():
    assert self.state == 0 #Contract still "created" which means item still up for sale?
    assert msg.value == (2*self.value) #Is the deposit of correct value?
    self.buyer = msg.sender
    self.state = 1 #Item is sold, seller cannot refund anymore
def recieved():
    assert self.state == 1 #Is the item already purchased and pending confirmation of buyer
    assert msg.sender == self.buyer 
    self.state = 2 #Contract finished. Unnecessary because of selfdestruct?
    send(self.buyer, self.value) #Return deposit to buyer
    selfdestruct(self.seller)

