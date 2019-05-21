import json
BpmElements=[
    ['BPM'],       
    ['BSM'],      
    ['BTM'], 
    ['BCM'],   
    ['BRQ'],     
    ['BAM','Secondarylevelmessages'],  
    ['FOM','Secondarylevelmessages'],  
    ['FCM','Secondarylevelmessages'],  
    ['FMM','Secondarylevelmessages'],  
    ['DBM','Secondarylevelmessages'],       
    ['CHG','ChangeStatus'], 
    ['DEL','ChangeStatus'],                                                                          #Standard Message Identifier                      
    ['.A', 'aElementIdentifier', 'aSenderMessRefNum', 'aBagMessageType', 'aACKorNAK', 'aFreeText'],    #.A:Message Acknowledgement details
    ['.V', 'vVerNumBagSourceAirportCode', 'vPartNum', 'vMesRefNum', 'vAckmtRequest', 'vEncryption'],    #.V:Version and Supplementary data                                        
    ['.J', 'jSecondaryCode', 'jAgentId', 'jScannerId', 'jProceDate', 'jProceTime', 'jReadLoc', 'jSentToLoc', 'jProceA', 'jProceB'],                                            #.J:Processing Information
    ['.F', 'fOutboundFlightAirlineFlightNum', 'fOutboundFlightDate', 'fOutboundFlightAirportCode', 'fClassTravelBag'],                                                                                            #.F:Outbound Flight Information
    ['.U', 'uStowageDeviceID', 'uAircraftLoadingLoc', 'uTypeBagLoc', 'uClassTravelBag', 'uAirportCodeContainer1', 'uSealedContainerIndicator', 'uConnectionAirlineCodeFlightNum', 'uConnectionDepartureDate', 'uAirportCodeContainer2'], #.U:Loading Data
    ['.N', 'nBagTagNum', 'nNumOfConsecutiveTags'],                            #.N:Baggage Tag Details
    ['.B', 'bBagStatusCode', 'bBagTagNum', 'bNumOfConsecutiveTags'], #.B:Baggage Irregularities
    ['.D', 'dBagCheckInLocId', 'dBagCheckInLocDesc', 'dBagCheckInDate', 'dBagCheckInTime', 'dCarriageMedium', 'dTransportID'],                                      #.D:Bag Check-in Location details
    ['.Q', 'qLoadSeqNum'],                                                    #.Q:Load Sequence Number
    ['.I', 'iInboundAirlineFlightNum', 'iInboundDate', 'iInboundAirportCode', 'iClassTravelBag'],  #.I:Inbound Flight Information
    ['.O', 'oOnwardAirlineFlightNum', 'oOnwardDate', 'oOnwardAirportCode', 'oClassTravelBag'],    #.O:Onward Flight Information
    ['.S', 'sAuzToLoad', 'sSeatNum', 'sPassStatus', 'sSequenceNum', 'sScyNum', 'sPassProfileStatus', 'sAuzToTransport', 'sBagTagStatus' ],                          #.S:Reconciliation Data
    ['.H', 'hTerminal', 'hBayPier', 'hGate'],           #.H:Handling Location
    ['.W', 'wWtInd', 'wNumberCheckedBags', 'wCheckedWt', 'wUncheckedWt', 'wUnit', 'wBagLen', 'wbagWidth', 'wbagHeight', 'wBagType'],                #.W:Pieces, Weight, Dimensions and Type Data
    ['.P', 'pSeparatorOblique', 'pNumberSurname', 'pGivenName', 'pAdditionalGivenName'], #.P:Passenger Name
    ['.G', 'gEarliestDDT', 'gLatestDDT', 'gAddLocDesc'],                  #.G:Ground Transport
    ['.Y', 'yFreTravellerIdNum', 'yTierId'],                          #.Y:Frequent Traveller Number
    ['.C', 'cCorpName'], #.C:Corporate or Group Name
    ['.T', 'tBagTagPrinterID'],     #.T:Baggage Tag Printer ID
    ['.E', 'eExcType'],           #.E:Baggage Exception Data
    ['.R', 'rFreeText'],               #.R:Internal Airline Data
    ['.X', 'xBagScyScreenINS', 'xScyScreenRs', 'xScyScreenRsReason', 'xScyScreenMethod', 'xAutograph', 'xFreeText'],                                    #.X:Baggage Security Screening
    ['.M', 'mBagTagNumLPN', 'mIdType', 'mId', 'mLink'], #.M:Unique Identifier
    ['ENDBPM'],                                        #End of Message Identifier
    ['ENDBSM'],                                        #End of Message Identifier
    ['ENDBTM'],                                        #End of Message Identifier
    ['ENDBCM'],                                        #End of Message Identifier
    ['ENDBRQ'],                                        #End of Message Identifier
    ['ENDPART']                                        #End of PART
]

BpmElementsDescription=[
    ['BPM'],       
    ['BSM'],        
    ['BTM'],            
    ['BCM'],     
    ['BRQ'],     
    ['BAM','Secondary level messages'],  
    ['FOM','Secondary level messages'],  
    ['FCM','Secondary level messages'],  
    ['FMM','Secondary level messages'],  
    ['DBM','Secondary level messages'],  
    ['CHG','Change of Status Indicator'], 
    ['DEL','Change of Status Indicator'],                                                                   #Standard Message Identifier                     
    ['.A', 'Element identifier', 'Senders Message Reference Number', 'Type of Baggage Message and Status Indicator being acknowledged', 'ACK or NAK', 'Free Text'],    #.A:Message Acknowledgement details
    ['.V', 'ex:1LFRA;1:Data Dictionary Version Number;L:Baggage Source;FRA:Local, Transfer or terminating Airport Code', 'Part Number', 'Message Reference Number', 'Acknowledgement Request', 'Encryption'],    #.V:Version and Supplementary data                                         
    ['.J', 'Secondary Code', 'Agent Identification', 'Scanner Identification', 'Date', 'Time', 'Reading Location', 'Sent to Location', 'ProcessingA', 'ProcessingB'],                                            #.J:Processing Information
    ['.F', 'Airline and Flight Number', 'Date', 'Destination or Transfer Airport Code', 'Class of Travel of Baggage'],                                                                                           #.F:Outbound Flight Information
    ['.U', 'Stowage Device ID', 'Aircraft Compartment Or Loading Location', 'Type Of Baggage in Container/Location', 'Class(es) of travel of Baggage', 'Destination or Transfer Airport Code of the Container', 'Sealed Container Indicator', 'Connection Airline Code and Flight Number', 'Connection Departure Date', 'Destination or transfer Airport Code of the Container'], #.U:Loading Data
    ['.N', 'Bag Tag Number', 'Number Of Consecutive Tags'],                            #.N:Baggage Tag Details
    ['.B', 'Baggage Status Code', 'Baggage Tag Number', 'Number Of Consecutive Tags'], #.B:Baggage Irregularities
    ['.D', 'Bag Check in location identifier', 'Bag Check in location description', 'Bag Check in date', 'Bag Check in Time', 'Carriage Medium', 'Transport ID(Free Text)'],                                     #.D:Bag Check-in Location details
    ['.Q', 'Load Sequence Number'],                                                    #.Q:Load Sequence Number
    ['.I', 'Airline and Flight Number', 'Date of Departure', 'Originating Airport Code', 'Class of Travel of Baggage'],  #.I:Inbound Flight Information
    ['.O', 'Airline and Flight Number', 'Date', 'Destination Or Transfer Airport Code', 'Class of Travel of Baggage'],   #.O:Onward Flight Information
    ['.S', 'Authority To Load', 'Seat Number', 'Passenger Status', 'Sequence Number', 'Security Number', 'Passenger Profile Status', 'Authority to Transport', 'Baggage Tag Status' ],                           #.S:Reconciliation Data
    ['.H', 'Handling Terminal', 'Handling Bay/Pier', 'Handling Gate/Stand'],           #.H:Handling Location
    ['.W', 'Pieces/Weight Indicator', 'Number of Checked Bags', 'Checked Weight', 'Unchecked Weight', 'Unit', 'Length of the bag', 'Width of the bag', 'Height of the bag', 'Baggage Type code'],                #.W:Pieces, Weight, Dimensions and Type Data
    ['.P', 'separator(oblique)', '2GROBET;2:Number of passengers with this surname;GROBET:Passengers Surname', 'Given Name and/or Initials and/or Title', 'Additional Given Name and/or Initials and/or Title'], #.P:Passenger Name
    ['.G', 'Earliest Delivery date/time', 'Latest Delivery date/time', 'Address/Location Description'],                 #.G:Ground Transport
    ['.Y', 'Frequent Traveller ID Number', 'Tier Identifier'],                         #.Y:Frequent Traveller Number
    ['.C', 'Corporate or Group Name'], #.C:Corporate or Group Name
    ['.T', 'Bag Tag Printer ID'],      #.T:Baggage Tag Printer ID
    ['.E', 'Exception Type'],          #.E:Baggage Exception Data
    ['.R', 'Free Text'],               #.R:Internal Airline Data
    ['.X', 'Baggage Security Screening Instruction', 'Security Screening Result', 'Security Screening Result Reason', 'Security Screening Method', 'Autograph', 'Free Text'],                                   #.X:Baggage Security Screening
    ['.M', 'Baggage Tag Number(LPN)', 'ID type', 'ID', 'Link'], #.M:Unique Identifier
    ['ENDBPM'],                                                 #End of Message Identifier
    ['ENDBSM'],                                                 #End of Message Identifier
    ['ENDBTM'],                                                 #End of Message Identifier
    ['ENDBCM'],                                                 #End of Message Identifier
    ['ENDBRQ'],                                        #End of Message Identifier
    ['ENDPART']                                                 #End of PART   
]

message = ''

for iBpmElementsRowIndex in range(len(BpmElements)):
    for iBpmElementsColumnIndex in range(len(BpmElements[iBpmElementsRowIndex])):
        print(BpmElements[iBpmElementsRowIndex][iBpmElementsColumnIndex],"//", BpmElementsDescription[iBpmElementsRowIndex][iBpmElementsColumnIndex]  )
        


#print(BpmElements[12][2])
#print(BpmElementsDescription[12][2])

# txt = "BPM\r\n.V/1LTPE\r\n.J/R///18APR/105210L/TIAT2/\r\n.F/OZ0712/18APR/ICN/Y\r\n.U/AKE25219OZ/TPE/X/Y/ICN///\r\n.N/0988401338001\r\n.Q/005\r\n.S/Y/25K/C/158/158//N\r\n.W/K/2/20\r\n.P/LU/CHINMEIMS\r\nENDBPM"
#txt = "BPM\r\n.V/1LTPE\r\n.J/R///18APR/002903L/TIAT2/\r\n.F/BR0026/17APR/SEA/Y\r\n.B/UNS/0695463055001\r\n.I/BR0266/17APR/PNH/Y\r\n.S/Y/70D/C/080/080//Y/A\r\n.W/K/1/17\r\n.P/ROS/SARAMONICH\r\nENDBPM"
#txt = "BSM\r\nCHG\r\n.V/1LZRH////123ABC456Z\r\n.F/SR101/18APR/JFK/C\r\n.N/0085123457001\r\n.S/N\r\nENDBSM"
#txt = "BTM\r\nDEL\r\n.V/1TJFK////123ABC4567\r\n.I/SR101/18APR/JFK/C\r\n.F/DL671/18APR/ATL/C\r\n.N/0085123457001\r\nENDBTM"
#txt = "BCM\r\nBAM\r\n.V/1LFRA\r\n.A/BA2190164/BSM DEL/ACK\r\nENDBCM"
txt = "BRQ\r\n.V/1LJFK\r\n.F/LH401/18APR/FRA/Y\r\n.N/4220168055\r\n.H/T4/GREEN/K150\r\n.E/TGRQ\r\n.M/4220168055/X/E200341201324FC0A003760E18454254\r\nENDBRQ"

sBpmList = txt.split("\r\n", )
print(sBpmList)

sJson ='{'
txt = txt.replace("\r",'\\r')
txt = txt.replace("\n",'\\n')
sJson = sJson + '"Rawdata":'+'"'+txt+'"'

for iRowIndex in range(len(sBpmList)):
    #print (sBpmList[iRowIndex])
    column =sBpmList[iRowIndex].split("/", )
    
    for iBpmElementsRowIndex in range(len(BpmElements)):
        if column[0] == BpmElements[iBpmElementsRowIndex][0]:
            #print(iBpmElementsRowIndex,column[0]+"="+BpmElements[iBpmElementsRowIndex][0])
            break  
        
    for icolumnIndex in range(len(column)): 
        if icolumnIndex != 0 and column[icolumnIndex] :  
            if len(sJson) != 1:
                sJson = sJson +","
            sJson = sJson + '"'+ BpmElements[iBpmElementsRowIndex][icolumnIndex]+'":'+'"'+column[icolumnIndex]+'"'
            print(iRowIndex,icolumnIndex,'"'+BpmElements[iBpmElementsRowIndex][icolumnIndex]+'":'+'"'+column[icolumnIndex]+'"',"//", BpmElementsDescription[iBpmElementsRowIndex][icolumnIndex]  )
        else:
            if icolumnIndex == 0 and column[icolumnIndex] :
                if column[0]  == 'CHG' or column[0]  == 'DEL' :
                    if len(sJson) != 1:
                        sJson = sJson +","
                    sJson = sJson + '"'+ BpmElements[iBpmElementsRowIndex][icolumnIndex+1]+'":'+'"'+column[icolumnIndex]+'"'
                    print(iRowIndex,icolumnIndex,'"'+BpmElements[iBpmElementsRowIndex][icolumnIndex+1]+'":'+'"'+column[icolumnIndex]+'"',"//", BpmElementsDescription[iBpmElementsRowIndex][icolumnIndex+1]  )
                else:
                    if column[0]  == 'BPM' or column[0]  == 'BSM':                        
                        message = str(column[0])
            

sJson = sJson +'}'

#Processing
print (sJson)
BpmJson = json.loads(sJson)

process = ''
if message  == 'BPM':        
    if 'jProceA' in BpmJson:
        process = process + BpmJson['jProceA']
    if 'jProceB' in BpmJson:
        process = process + BpmJson['jProceB']
    if 'nBagTagNum' in BpmJson:
        if process == '':
            process = process + "MU"   
    if 'bBagTagNum' in BpmJson:    
        if process == '':
            process = process + "MUB"    
        else:
            process =  process + "B"   
    BpmJson.update( {"Processing":process} )


BagPrimarykey = ''
if 'nBagTagNum' in BpmJson: 
    if BagPrimarykey == '':
        BagPrimarykey = BagPrimarykey + BpmJson['nBagTagNum']
if 'bBagTagNum' in BpmJson:      
    if BagPrimarykey == '':
        BagPrimarykey = BagPrimarykey + BpmJson['bBagTagNum']                   


if 'fOutboundFlightAirlineFlightNum' in BpmJson:   
    BagPrimarykey = BagPrimarykey + BpmJson['fOutboundFlightAirlineFlightNum']
if 'fOutboundFlightDate' in BpmJson:         
    BagPrimarykey = BagPrimarykey + BpmJson['fOutboundFlightDate']
if 'fOutboundFlightAirportCode' in BpmJson:  
    BagPrimarykey = BagPrimarykey + BpmJson['fOutboundFlightAirportCode']
if BagPrimarykey != "":
    BpmJson.update( {"BagPrimarykey":BagPrimarykey} )

#print(type(person)) #<class 'dict'>
#print(BpmJson['vVerNumBagSourceAirportCode']) #25
 
json_str = json.dumps(BpmJson)
print ("JSON 对象：", json_str)
 


