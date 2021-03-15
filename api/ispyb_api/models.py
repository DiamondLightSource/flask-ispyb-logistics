# coding: utf-8
from sqlalchemy import BINARY, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.ext.declarative import declarative_base


from . import Base


class BLSession(Base):
    __tablename__ = 'BLSession'
    __table_args__ = (
        Index('proposalId', 'proposalId', 'visit_number', unique=True),
    )

    sessionId = Column(Integer, primary_key=True)
    beamLineSetupId = Column(ForeignKey(u'BeamLineSetup.beamLineSetupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), nullable=False, index=True, server_default=text("0"))
    beamCalendarId = Column(ForeignKey(u'BeamCalendar.beamCalendarId'), index=True)
    projectCode = Column(String(45))
    startDate = Column(DateTime, index=True)
    endDate = Column(DateTime, index=True)
    beamLineName = Column(String(45), index=True)
    scheduled = Column(Integer)
    nbShifts = Column(Integer)
    comments = Column(String(2000))
    beamLineOperator = Column(String(255))
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    visit_number = Column(Integer, server_default=text("0"))
    usedFlag = Column(Integer)
    sessionTitle = Column(String(255))
    structureDeterminations = Column(Float)
    dewarTransport = Column(Float)
    databackupFrance = Column(Float)
    databackupEurope = Column(Float)
    expSessionPk = Column(Integer)
    operatorSiteNumber = Column(String(10), index=True)
    lastUpdate = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    protectedData = Column(String(1024))
    externalId = Column(BINARY(16))
    archived = Column(Integer, server_default=text("0"))

    BeamCalendar = relationship(u'BeamCalendar')
    BeamLineSetup = relationship(u'BeamLineSetup')
    Proposal = relationship(u'Proposal')


class BeamCalendar(Base):
    __tablename__ = 'BeamCalendar'

    beamCalendarId = Column(Integer, primary_key=True)
    run = Column(String(7), nullable=False)
    beamStatus = Column(String(24), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)


class BeamLineSetup(Base):
    __tablename__ = 'BeamLineSetup'

    beamLineSetupId = Column(Integer, primary_key=True)
    detectorId = Column(ForeignKey(u'Detector.detectorId'), index=True)
    synchrotronMode = Column(String(255))
    undulatorType1 = Column(String(45))
    undulatorType2 = Column(String(45))
    undulatorType3 = Column(String(45))
    focalSpotSizeAtSample = Column(Float)
    focusingOptic = Column(String(255))
    beamDivergenceHorizontal = Column(Float)
    beamDivergenceVertical = Column(Float)
    polarisation = Column(Float)
    monochromatorType = Column(String(255))
    setupDate = Column(DateTime)
    synchrotronName = Column(String(255))
    maxExpTimePerDataCollection = Column(Float(asdecimal=True))
    maxExposureTimePerImage = Column(Float)
    minExposureTimePerImage = Column(Float(asdecimal=True))
    goniostatMaxOscillationSpeed = Column(Float(asdecimal=True))
    goniostatMaxOscillationWidth = Column(Float(asdecimal=True))
    goniostatMinOscillationWidth = Column(Float(asdecimal=True))
    maxTransmission = Column(Float(asdecimal=True))
    minTransmission = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    CS = Column(Float)
    beamlineName = Column(String(50))
    beamSizeXMin = Column(Float)
    beamSizeXMax = Column(Float)
    beamSizeYMin = Column(Float)
    beamSizeYMax = Column(Float)
    energyMin = Column(Float)
    energyMax = Column(Float)
    omegaMin = Column(Float)
    omegaMax = Column(Float)
    kappaMin = Column(Float)
    kappaMax = Column(Float)
    phiMin = Column(Float)
    phiMax = Column(Float)
    active = Column(Integer, nullable=False, server_default=text("0"))
    numberOfImagesMax = Column(Integer)
    numberOfImagesMin = Column(Integer)
    boxSizeXMin = Column(Float(asdecimal=True))
    boxSizeXMax = Column(Float(asdecimal=True))
    boxSizeYMin = Column(Float(asdecimal=True))
    boxSizeYMax = Column(Float(asdecimal=True))
    monoBandwidthMin = Column(Float(asdecimal=True))
    monoBandwidthMax = Column(Float(asdecimal=True))

    Detector = relationship(u'Detector')


class Detector(Base):
    __tablename__ = 'Detector'
    __table_args__ = (
        Index('Detector_FKIndex1', 'detectorType', 'detectorManufacturer', 'detectorModel', 'detectorPixelSizeHorizontal', 'detectorPixelSizeVertical'),
    )

    detectorId = Column(Integer, primary_key=True)
    detectorType = Column(String(255))
    detectorManufacturer = Column(String(255))
    detectorModel = Column(String(255))
    detectorPixelSizeHorizontal = Column(Float)
    detectorPixelSizeVertical = Column(Float)
    DETECTORMAXRESOLUTION = Column(Float)
    DETECTORMINRESOLUTION = Column(Float)
    detectorSerialNumber = Column(String(30), unique=True)
    detectorDistanceMin = Column(Float(asdecimal=True))
    detectorDistanceMax = Column(Float(asdecimal=True))
    trustedPixelValueRangeLower = Column(Float(asdecimal=True))
    trustedPixelValueRangeUpper = Column(Float(asdecimal=True))
    sensorThickness = Column(Float)
    overload = Column(Float)
    XGeoCorr = Column(String(255))
    YGeoCorr = Column(String(255))
    detectorMode = Column(String(255))
    density = Column(Float)
    composition = Column(String(16))
    numberOfPixelsX = Column(Integer)
    numberOfPixelsY = Column(Integer)
    detectorRollMin = Column(Float(asdecimal=True))
    detectorRollMax = Column(Float(asdecimal=True))
    localName = Column(String(40))


class Dewar(Base):
    __tablename__ = 'Dewar'

    dewarId = Column(Integer, primary_key=True)
    shippingId = Column(ForeignKey(u'Shipping.shippingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    code = Column(String(45), index=True)
    comments = Column(String)
    storageLocation = Column(String(45))
    dewarStatus = Column(String(45), index=True)
    bltimeStamp = Column(DateTime)
    isStorageDewar = Column(Integer, server_default=text("0"))
    barCode = Column(String(45), unique=True)
    firstExperimentId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    customsValue = Column(Integer)
    transportValue = Column(Integer)
    trackingNumberToSynchrotron = Column(String(30))
    trackingNumberFromSynchrotron = Column(String(30))
    type = Column(ENUM(u'Dewar', u'Toolbox'), nullable=False, server_default=text("'Dewar'"))
    FACILITYCODE = Column(String(20))
    weight = Column(Float)
    deliveryAgent_barcode = Column(String(30))

    BLSession = relationship(u'BLSession')
    Shipping = relationship(u'Shipping')


class DewarTransportHistory(Base):
    __tablename__ = 'DewarTransportHistory'

    DewarTransportHistoryId = Column(Integer, primary_key=True)
    dewarId = Column(ForeignKey(u'Dewar.dewarId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    dewarStatus = Column(String(45), nullable=False)
    storageLocation = Column(String(45))
    arrivalDate = Column(DateTime)

    Dewar = relationship(u'Dewar')


class LabContact(Base):
    __tablename__ = 'LabContact'
    __table_args__ = (
        Index('cardNameAndProposal', 'cardName', 'proposalId', unique=True),
        Index('personAndProposal', 'personId', 'proposalId', unique=True)
    )

    labContactId = Column(Integer, primary_key=True)
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    cardName = Column(String(40), nullable=False)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), nullable=False, index=True)
    defaultCourrierCompany = Column(String(45))
    courierAccount = Column(String(45))
    billingReference = Column(String(45))
    dewarAvgCustomsValue = Column(Integer, nullable=False, server_default=text("0"))
    dewarAvgTransportValue = Column(Integer, nullable=False, server_default=text("0"))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')


class Laboratory(Base):
    __tablename__ = 'Laboratory'

    laboratoryId = Column(Integer, primary_key=True)
    laboratoryUUID = Column(String(45))
    name = Column(String(45))
    address = Column(String(255))
    city = Column(String(45))
    country = Column(String(45))
    url = Column(String(255))
    organization = Column(String(45))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    postcode = Column(String(15))


class Person(Base):
    __tablename__ = 'Person'

    personId = Column(Integer, primary_key=True)
    laboratoryId = Column(ForeignKey(u'Laboratory.laboratoryId'), index=True)
    siteId = Column(Integer, index=True)
    personUUID = Column(String(45))
    familyName = Column(String(100, u'utf8mb4_unicode_ci'), index=True)
    givenName = Column(String(45, u'utf8mb4_unicode_ci'))
    title = Column(String(45))
    emailAddress = Column(String(60))
    phoneNumber = Column(String(45))
    login = Column(String(45), unique=True)
    faxNumber = Column(String(45))
    cache = Column(Text)
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    externalId = Column(BINARY(16))

    Laboratory = relationship(u'Laboratory')


class Proposal(Base):
    __tablename__ = 'Proposal'
    __table_args__ = (
        Index('Proposal_FKIndexCodeNumber', 'proposalCode', 'proposalNumber', unique=True),
    )

    proposalId = Column(Integer, primary_key=True)
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("0"))
    title = Column(String(255, u'utf8mb4_unicode_ci'))
    proposalCode = Column(String(45))
    proposalNumber = Column(String(45))
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    proposalType = Column(String(2))
    externalId = Column(BINARY(16))
    state = Column(ENUM(u'Open', u'Closed', u'Cancelled'), server_default=text("'Open'"))

    Person = relationship(u'Person')


class Shipping(Base):
    __tablename__ = 'Shipping'

    shippingId = Column(Integer, primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), nullable=False, index=True, server_default=text("0"))
    shippingName = Column(String(45), index=True)
    deliveryAgent_agentName = Column(String(45))
    deliveryAgent_shippingDate = Column(Date)
    deliveryAgent_deliveryDate = Column(Date)
    deliveryAgent_agentCode = Column(String(45))
    deliveryAgent_flightCode = Column(String(45))
    shippingStatus = Column(String(45), index=True)
    bltimeStamp = Column(DateTime)
    laboratoryId = Column(Integer, index=True)
    isStorageShipping = Column(Integer, server_default=text("0"))
    creationDate = Column(DateTime, index=True)
    comments = Column(String(255))
    sendingLabContactId = Column(ForeignKey(u'LabContact.labContactId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    returnLabContactId = Column(ForeignKey(u'LabContact.labContactId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    returnCourier = Column(String(45))
    dateOfShippingToUser = Column(DateTime)
    shippingType = Column(String(45))
    SAFETYLEVEL = Column(String(8))
    deliveryAgent_flightCodeTimestamp = Column(DateTime)
    deliveryAgent_label = Column(Text)
    readyByTime = Column(Time)
    closeTime = Column(Time)
    physicalLocation = Column(String(50))
    deliveryAgent_pickupConfirmationTimestamp = Column(DateTime)
    deliveryAgent_pickupConfirmation = Column(String(10))
    deliveryAgent_readyByTime = Column(Time)
    deliveryAgent_callinTime = Column(Time)
    deliveryAgent_productCode = Column(String(10))
    deliveryAgent_flightCodePersonId = Column(ForeignKey(u'Person.personId'), index=True)

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')
    LabContact = relationship(u'LabContact', primaryjoin='Shipping.returnLabContactId == LabContact.labContactId')
    LabContact1 = relationship(u'LabContact', primaryjoin='Shipping.sendingLabContactId == LabContact.labContactId')
