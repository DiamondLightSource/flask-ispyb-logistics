# coding: utf-8
from sqlalchemy import BINARY, BigInteger, Column, Date, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.dialects.mysql.types import LONGBLOB

# If using this as a models file in sqlalchemy (not flask)
#from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()

from . import Base

class AbInitioModel(Base):
    __tablename__ = 'AbInitioModel'

    abInitioModelId = Column(Integer, primary_key=True)
    modelListId = Column(ForeignKey(u'ModelList.modelListId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    averagedModelId = Column(ForeignKey(u'Model.modelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    rapidShapeDeterminationModelId = Column(ForeignKey(u'Model.modelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    shapeDeterminationModelId = Column(ForeignKey(u'Model.modelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    comments = Column(String(512))
    creationTime = Column(DateTime)

    Model = relationship(u'Model', primaryjoin='AbInitioModel.averagedModelId == Model.modelId')
    ModelList = relationship(u'ModelList')
    Model1 = relationship(u'Model', primaryjoin='AbInitioModel.rapidShapeDeterminationModelId == Model.modelId')
    Model2 = relationship(u'Model', primaryjoin='AbInitioModel.shapeDeterminationModelId == Model.modelId')


class Additive(Base):
    __tablename__ = 'Additive'

    additiveId = Column(Integer, primary_key=True)
    name = Column(String(45))
    additiveType = Column(String(45))
    comments = Column(String(512))


class AdminActivity(Base):
    __tablename__ = 'AdminActivity'

    adminActivityId = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False, unique=True, server_default=text("''"))
    action = Column(String(45), index=True)
    comments = Column(String(100))
    dateTime = Column(DateTime)


class AdminVar(Base):
    __tablename__ = 'AdminVar'

    varId = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    value = Column(String(1024), index=True)


class Aperture(Base):
    __tablename__ = 'Aperture'

    apertureId = Column(Integer, primary_key=True)
    sizeX = Column(Float)


class Assembly(Base):
    __tablename__ = 'Assembly'

    assemblyId = Column(Integer, primary_key=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    creationDate = Column(DateTime)
    comments = Column(String(255))

    Macromolecule = relationship(u'Macromolecule')


class AssemblyHasMacromolecule(Base):
    __tablename__ = 'AssemblyHasMacromolecule'

    AssemblyHasMacromoleculeId = Column(Integer, primary_key=True)
    assemblyId = Column(ForeignKey(u'Assembly.assemblyId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    Assembly = relationship(u'Assembly')
    Macromolecule = relationship(u'Macromolecule')


class AssemblyRegion(Base):
    __tablename__ = 'AssemblyRegion'

    assemblyRegionId = Column(Integer, primary_key=True)
    assemblyHasMacromoleculeId = Column(ForeignKey(u'AssemblyHasMacromolecule.AssemblyHasMacromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    assemblyRegionType = Column(String(45))
    name = Column(String(45))
    fromResiduesBases = Column(String(45))
    toResiduesBases = Column(String(45))

    AssemblyHasMacromolecule = relationship(u'AssemblyHasMacromolecule')


class AutoProc(Base):
    __tablename__ = 'AutoProc'

    autoProcId = Column(Integer, primary_key=True)
    autoProcProgramId = Column(Integer, index=True)
    spaceGroup = Column(String(45))
    refinedCell_a = Column(Float)
    refinedCell_b = Column(Float)
    refinedCell_c = Column(Float)
    refinedCell_alpha = Column(Float)
    refinedCell_beta = Column(Float)
    refinedCell_gamma = Column(Float)
    recordTimeStamp = Column(DateTime)


class AutoProcIntegration(Base):
    __tablename__ = 'AutoProcIntegration'

    autoProcIntegrationId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    startImageNumber = Column(Integer)
    endImageNumber = Column(Integer)
    refinedDetectorDistance = Column(Float)
    refinedXBeam = Column(Float)
    refinedYBeam = Column(Float)
    rotationAxisX = Column(Float)
    rotationAxisY = Column(Float)
    rotationAxisZ = Column(Float)
    beamVectorX = Column(Float)
    beamVectorY = Column(Float)
    beamVectorZ = Column(Float)
    cell_a = Column(Float)
    cell_b = Column(Float)
    cell_c = Column(Float)
    cell_alpha = Column(Float)
    cell_beta = Column(Float)
    cell_gamma = Column(Float)
    recordTimeStamp = Column(DateTime)
    anomalous = Column(Integer, server_default=text("'0'"))

    AutoProcProgram = relationship(u'AutoProcProgram')
    DataCollection = relationship(u'DataCollection')


class AutoProcProgram(Base):
    __tablename__ = 'AutoProcProgram'

    autoProcProgramId = Column(Integer, primary_key=True)
    processingCommandLine = Column(String(255))
    processingPrograms = Column(String(255))
    processingStatus = Column(Integer)
    processingMessage = Column(String(255))
    processingStartTime = Column(DateTime)
    processingEndTime = Column(DateTime)
    processingEnvironment = Column(String(255))
    recordTimeStamp = Column(DateTime)
    processingJobId = Column(ForeignKey(u'ProcessingJob.processingJobId'), index=True)

    ProcessingJob = relationship(u'ProcessingJob')


class AutoProcProgramAttachment(Base):
    __tablename__ = 'AutoProcProgramAttachment'

    autoProcProgramAttachmentId = Column(Integer, primary_key=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    fileType = Column(ENUM(u'Log', u'Result', u'Graph'))
    fileName = Column(String(255))
    filePath = Column(String(255))
    recordTimeStamp = Column(DateTime)

    AutoProcProgram = relationship(u'AutoProcProgram')


class AutoProcScaling(Base):
    __tablename__ = 'AutoProcScaling'
    __table_args__ = (
        Index('AutoProcScalingIdx1', 'autoProcScalingId', 'autoProcId'),
    )

    autoProcScalingId = Column(Integer, primary_key=True)
    autoProcId = Column(ForeignKey(u'AutoProc.autoProcId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    recordTimeStamp = Column(DateTime)

    AutoProc = relationship(u'AutoProc')


class AutoProcScalingStatistic(Base):
    __tablename__ = 'AutoProcScalingStatistics'

    autoProcScalingStatisticsId = Column(Integer, primary_key=True)
    autoProcScalingId = Column(ForeignKey(u'AutoProcScaling.autoProcScalingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    scalingStatisticsType = Column(ENUM(u'overall', u'innerShell', u'outerShell'), nullable=False, index=True, server_default=text("'overall'"))
    comments = Column(String(255))
    resolutionLimitLow = Column(Float)
    resolutionLimitHigh = Column(Float)
    rMerge = Column(Float)
    rMeasWithinIPlusIMinus = Column(Float)
    rMeasAllIPlusIMinus = Column(Float)
    rPimWithinIPlusIMinus = Column(Float)
    rPimAllIPlusIMinus = Column(Float)
    fractionalPartialBias = Column(Float)
    nTotalObservations = Column(Integer)
    nTotalUniqueObservations = Column(Integer)
    meanIOverSigI = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    anomalousCompleteness = Column(Float)
    anomalousMultiplicity = Column(Float)
    recordTimeStamp = Column(DateTime)
    anomalous = Column(Integer, server_default=text("'0'"))
    ccHalf = Column(Float)
    ccAnomalous = Column(Float)

    AutoProcScaling = relationship(u'AutoProcScaling')


class AutoProcScalingHasInt(Base):
    __tablename__ = 'AutoProcScaling_has_Int'
    __table_args__ = (
        Index('AutoProcScalingHasInt_FKIndex3', 'autoProcScalingId', 'autoProcIntegrationId'),
    )

    autoProcScaling_has_IntId = Column(Integer, primary_key=True)
    autoProcScalingId = Column(ForeignKey(u'AutoProcScaling.autoProcScalingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    autoProcIntegrationId = Column(ForeignKey(u'AutoProcIntegration.autoProcIntegrationId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    recordTimeStamp = Column(DateTime)

    AutoProcIntegration = relationship(u'AutoProcIntegration')
    AutoProcScaling = relationship(u'AutoProcScaling')


class AutoProcStatu(Base):
    __tablename__ = 'AutoProcStatus'

    autoProcStatusId = Column(Integer, primary_key=True)
    autoProcIntegrationId = Column(ForeignKey(u'AutoProcIntegration.autoProcIntegrationId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    step = Column(ENUM(u'Indexing', u'Integration', u'Correction', u'Scaling', u'Importing'), nullable=False)
    status = Column(ENUM(u'Launched', u'Successful', u'Failed'), nullable=False)
    comments = Column(String(1024))
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    AutoProcIntegration = relationship(u'AutoProcIntegration')


class BFComponent(Base):
    __tablename__ = 'BF_component'

    componentId = Column(Integer, primary_key=True)
    systemId = Column(ForeignKey(u'BF_system.systemId'), index=True)
    name = Column(String(100))
    description = Column(String(200))

    BF_system = relationship(u'BFSystem')


class BFComponentBeamline(Base):
    __tablename__ = 'BF_component_beamline'

    component_beamlineId = Column(Integer, primary_key=True)
    componentId = Column(ForeignKey(u'BF_component.componentId'), index=True)
    beamlinename = Column(String(20))

    BF_component = relationship(u'BFComponent')


class BFFault(Base):
    __tablename__ = 'BF_fault'

    faultId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId'), nullable=False, index=True)
    owner = Column(String(50))
    subcomponentId = Column(ForeignKey(u'BF_subcomponent.subcomponentId'), index=True)
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    beamtimelost = Column(Integer)
    beamtimelost_starttime = Column(DateTime)
    beamtimelost_endtime = Column(DateTime)
    title = Column(String(200))
    description = Column(Text)
    resolved = Column(Integer)
    resolution = Column(Text)
    attachment = Column(String(200))
    eLogId = Column(Integer)
    assignee = Column(String(50))
    personId = Column(ForeignKey(u'Person.personId'), index=True)
    assigneeId = Column(ForeignKey(u'Person.personId'), index=True)

    Person = relationship(u'Person', primaryjoin='BFFault.assigneeId == Person.personId')
    Person1 = relationship(u'Person', primaryjoin='BFFault.personId == Person.personId')
    BLSession = relationship(u'BLSession')
    BF_subcomponent = relationship(u'BFSubcomponent')


class BFSubcomponent(Base):
    __tablename__ = 'BF_subcomponent'

    subcomponentId = Column(Integer, primary_key=True)
    componentId = Column(ForeignKey(u'BF_component.componentId'), index=True)
    name = Column(String(100))
    description = Column(String(200))

    BF_component = relationship(u'BFComponent')


class BFSubcomponentBeamline(Base):
    __tablename__ = 'BF_subcomponent_beamline'

    subcomponent_beamlineId = Column(Integer, primary_key=True)
    subcomponentId = Column(ForeignKey(u'BF_subcomponent.subcomponentId'), index=True)
    beamlinename = Column(String(20))

    BF_subcomponent = relationship(u'BFSubcomponent')


class BFSystem(Base):
    __tablename__ = 'BF_system'

    systemId = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))


class BFSystemBeamline(Base):
    __tablename__ = 'BF_system_beamline'

    system_beamlineId = Column(Integer, primary_key=True)
    systemId = Column(ForeignKey(u'BF_system.systemId'), index=True)
    beamlineName = Column(String(20))

    BF_system = relationship(u'BFSystem')


class BLSample(Base):
    __tablename__ = 'BLSample'
    __table_args__ = (
        Index('crystalId', 'crystalId', 'containerId'),
    )

    blSampleId = Column(Integer, primary_key=True)
    diffractionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    crystalId = Column(ForeignKey(u'Crystal.crystalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True, server_default=text("'0'"))
    containerId = Column(ForeignKey(u'Container.containerId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    name = Column(String(45), index=True)
    code = Column(String(45))
    location = Column(String(45))
    holderLength = Column(Float(asdecimal=True))
    loopLength = Column(Float(asdecimal=True))
    loopType = Column(String(45))
    wireWidth = Column(Float(asdecimal=True))
    comments = Column(String(1024))
    completionStage = Column(String(45))
    structureStage = Column(String(45))
    publicationStage = Column(String(45))
    publicationComments = Column(String(255))
    blSampleStatus = Column(String(20), index=True)
    isInSampleChanger = Column(Integer)
    lastKnownCenteringPosition = Column(String(255))
    POSITIONID = Column(Integer)
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    SMILES = Column(String(400))
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId'), index=True)
    lastImageURL = Column(String(255))
    screenComponentGroupId = Column(ForeignKey(u'ScreenComponentGroup.screenComponentGroupId'), index=True)
    volume = Column(Float)
    dimension1 = Column(Float(asdecimal=True))
    dimension2 = Column(Float(asdecimal=True))
    dimension3 = Column(Float(asdecimal=True))
    shape = Column(String(15))
    packingFraction = Column(Float)
    preparationTemeprature = Column(Integer)
    preparationHumidity = Column(Float)
    blottingTime = Column(Integer)
    blottingForce = Column(Float)
    blottingDrainTime = Column(Integer)
    support = Column(String(50))
    subLocation = Column(SmallInteger)

    BLSubSample = relationship(u'BLSubSample', primaryjoin='BLSample.blSubSampleId == BLSubSample.blSubSampleId')
    Container = relationship(u'Container')
    Crystal = relationship(u'Crystal')
    DiffractionPlan = relationship(u'DiffractionPlan')
    ScreenComponentGroup = relationship(u'ScreenComponentGroup')
    Project = relationship(u'Project', secondary='Project_has_BLSample')


class BLSampleGroup(Base):
    __tablename__ = 'BLSampleGroup'

    blSampleGroupId = Column(Integer, primary_key=True)


class BLSampleGroupHasBLSample(Base):
    __tablename__ = 'BLSampleGroup_has_BLSample'

    blSampleGroupId = Column(ForeignKey(u'BLSampleGroup.blSampleGroupId'), primary_key=True, nullable=False)
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId'), primary_key=True, nullable=False, index=True)
    groupOrder = Column(Integer)
    type = Column(ENUM(u'background', u'container', u'sample', u'calibrant'))

    BLSampleGroup = relationship(u'BLSampleGroup')
    BLSample = relationship(u'BLSample')


class BLSampleImage(Base):
    __tablename__ = 'BLSampleImage'

    blSampleImageId = Column(Integer, primary_key=True)
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId'), nullable=False, index=True)
    micronsPerPixelX = Column(Float)
    micronsPerPixelY = Column(Float)
    imageFullPath = Column(String(255))
    blSampleImageScoreId = Column(Integer)
    comments = Column(String(255))
    blTimeStamp = Column(DateTime)
    containerInspectionId = Column(ForeignKey(u'ContainerInspection.containerInspectionId'), index=True)
    modifiedTimeStamp = Column(DateTime)

    BLSample = relationship(u'BLSample')
    ContainerInspection = relationship(u'ContainerInspection')


class BLSampleImageAnalysi(Base):
    __tablename__ = 'BLSampleImageAnalysis'

    blSampleImageAnalysisId = Column(Integer, primary_key=True)
    blSampleImageId = Column(ForeignKey(u'BLSampleImage.blSampleImageId'), index=True)
    oavSnapshotBefore = Column(String(255))
    oavSnapshotAfter = Column(String(255))
    deltaX = Column(Integer)
    deltaY = Column(Integer)
    goodnessOfFit = Column(Float)
    scaleFactor = Column(Float)
    resultCode = Column(String(15))
    matchStartTimeStamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    matchEndTimeStamp = Column(DateTime)

    BLSampleImage = relationship(u'BLSampleImage')


class BLSampleImageMeasurement(Base):
    __tablename__ = 'BLSampleImageMeasurement'

    blSampleImageMeasurementId = Column(Integer, primary_key=True)
    blSampleImageId = Column(ForeignKey(u'BLSampleImage.blSampleImageId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId'), index=True)
    startPosX = Column(Float(asdecimal=True))
    startPosY = Column(Float(asdecimal=True))
    endPosX = Column(Float(asdecimal=True))
    endPosY = Column(Float(asdecimal=True))
    blTimeStamp = Column(DateTime)

    BLSampleImage = relationship(u'BLSampleImage')
    BLSubSample = relationship(u'BLSubSample')


class BLSampleImageScore(Base):
    __tablename__ = 'BLSampleImageScore'

    blSampleImageScoreId = Column(Integer, primary_key=True)
    name = Column(String(45))
    score = Column(Float)
    colour = Column(String(15))


class BLSampleTypeHasComponent(Base):
    __tablename__ = 'BLSampleType_has_Component'

    blSampleTypeId = Column(ForeignKey(u'Crystal.crystalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False)
    componentId = Column(ForeignKey(u'Protein.proteinId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
    abundance = Column(Float)

    Crystal = relationship(u'Crystal')
    Protein = relationship(u'Protein')


class BLSampleHasDataCollectionPlan(Base):
    __tablename__ = 'BLSample_has_DataCollectionPlan'

    blSampleId = Column(ForeignKey(u'BLSample.blSampleId'), primary_key=True, nullable=False)
    dataCollectionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId'), primary_key=True, nullable=False, index=True)
    planOrder = Column(Integer)

    BLSample = relationship(u'BLSample')
    DiffractionPlan = relationship(u'DiffractionPlan')


class BLSampleHasEnergyScan(Base):
    __tablename__ = 'BLSample_has_EnergyScan'

    blSampleId = Column(ForeignKey(u'BLSample.blSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    energyScanId = Column(ForeignKey(u'EnergyScan.energyScanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    blSampleHasEnergyScanId = Column(Integer, primary_key=True)

    BLSample = relationship(u'BLSample')
    EnergyScan = relationship(u'EnergyScan')


class BLSession(Base):
    __tablename__ = 'BLSession'

    sessionId = Column(Integer, primary_key=True)
    beamLineSetupId = Column(ForeignKey(u'BeamLineSetup.beamLineSetupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    projectCode = Column(String(45))
    startDate = Column(DateTime, index=True)
    endDate = Column(DateTime, index=True)
    beamLineName = Column(String(45), index=True)
    scheduled = Column(Integer)
    nbShifts = Column(Integer)
    comments = Column(String(2000))
    beamLineOperator = Column(String(45))
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    visit_number = Column(Integer, server_default=text("'0'"))
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

    BeamLineSetup = relationship(u'BeamLineSetup')
    Proposal = relationship(u'Proposal')
    Shipping = relationship(u'Shipping', secondary='ShippingHasSession')

    def __str__(self):
        return "{}{}-{}".format(self.Proposal.proposalCode, self.Proposal.proposalNumber, self.visit_number)


class BLSessionHasSCPosition(Base):
    __tablename__ = 'BLSession_has_SCPosition'

    blsessionhasscpositionid = Column(Integer, primary_key=True)
    blsessionid = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    scContainer = Column(SmallInteger)
    containerPosition = Column(SmallInteger)

    BLSession = relationship(u'BLSession')


class BLSubSample(Base):
    __tablename__ = 'BLSubSample'

    blSubSampleId = Column(Integer, primary_key=True)
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    diffractionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    blSampleImageId = Column(ForeignKey(u'BLSampleImage.blSampleImageId'), index=True)
    positionId = Column(ForeignKey(u'Position.positionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    position2Id = Column(ForeignKey(u'Position.positionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    motorPositionId = Column(ForeignKey(u'MotorPosition.motorPositionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    blSubSampleUUID = Column(String(45))
    imgFileName = Column(String(255))
    imgFilePath = Column(String(1024))
    comments = Column(String(1024))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    BLSample = relationship(u'BLSample', primaryjoin='BLSubSample.blSampleId == BLSample.blSampleId')
    BLSampleImage = relationship(u'BLSampleImage')
    DiffractionPlan = relationship(u'DiffractionPlan')
    MotorPosition = relationship(u'MotorPosition')
    Position = relationship(u'Position', primaryjoin='BLSubSample.position2Id == Position.positionId')
    Position1 = relationship(u'Position', primaryjoin='BLSubSample.positionId == Position.positionId')


class BeamAperture(Base):
    __tablename__ = 'BeamApertures'

    beamAperturesid = Column(Integer, primary_key=True)
    beamlineStatsId = Column(ForeignKey(u'BeamlineStats.beamlineStatsId', ondelete=u'CASCADE'), index=True)
    flux = Column(Float(asdecimal=True))
    x = Column(Float)
    y = Column(Float)
    apertureSize = Column(SmallInteger)

    BeamlineStat = relationship('BeamlineStat')


class BeamCalendar(Base):
    __tablename__ = 'BeamCalendar'

    beamCalendarId = Column(Integer, primary_key=True)
    run = Column(String(7), nullable=False)
    beamStatus = Column(String(24), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)


class BeamCentre(Base):
    __tablename__ = 'BeamCentres'

    beamCentresid = Column(Integer, primary_key=True)
    beamlineStatsId = Column(ForeignKey(u'BeamlineStats.beamlineStatsId', ondelete=u'CASCADE'), index=True)
    x = Column(Float)
    y = Column(Float)
    zoom = Column(Integer)

    BeamlineStat = relationship('BeamlineStat')


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
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
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
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    numberOfImagesMax = Column(Integer)
    numberOfImagesMin = Column(Integer)
    boxSizeXMin = Column(Float(asdecimal=True))
    boxSizeXMax = Column(Float(asdecimal=True))
    boxSizeYMin = Column(Float(asdecimal=True))
    boxSizeYMax = Column(Float(asdecimal=True))
    monoBandwidthMin = Column(Float(asdecimal=True))
    monoBandwidthMax = Column(Float(asdecimal=True))

    Detector = relationship(u'Detector')


class BeamlineAction(Base):
    __tablename__ = 'BeamlineAction'

    beamlineActionId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId'), index=True)
    startTimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    endTimestamp = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    message = Column(String(255))
    parameter = Column(String(50))
    value = Column(String(30))
    loglevel = Column(ENUM(u'DEBUG', u'CRITICAL', u'INFO'))
    status = Column(ENUM(u'PAUSED', u'RUNNING', u'TERMINATED', u'COMPLETE', u'ERROR', u'EPICSFAIL'))

    BLSession = relationship(u'BLSession')


class BeamlineStat(Base):
    __tablename__ = 'BeamlineStats'

    beamlineStatsId = Column(Integer, primary_key=True)
    beamline = Column(String(10))
    recordTimeStamp = Column(DateTime)
    ringCurrent = Column(Float)
    energy = Column(Float)
    gony = Column(Float)
    beamW = Column(Float)
    beamH = Column(Float)
    flux = Column(Float(asdecimal=True))
    scanFileW = Column(String(255))
    scanFileH = Column(String(255))


class Buffer(Base):
    __tablename__ = 'Buffer'

    bufferId = Column(Integer, primary_key=True)
    BLSESSIONID = Column(Integer)
    safetyLevelId = Column(ForeignKey(u'SafetyLevel.safetyLevelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    name = Column(String(45))
    acronym = Column(String(45))
    pH = Column(String(45))
    composition = Column(String(45))
    comments = Column(String(512))
    proposalId = Column(Integer, nullable=False, server_default=text("'-1'"))

    SafetyLevel = relationship(u'SafetyLevel')


class BufferHasAdditive(Base):
    __tablename__ = 'BufferHasAdditive'

    bufferHasAdditiveId = Column(Integer, primary_key=True)
    bufferId = Column(ForeignKey(u'Buffer.bufferId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    additiveId = Column(ForeignKey(u'Additive.additiveId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    measurementUnitId = Column(ForeignKey(u'MeasurementUnit.measurementUnitId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    quantity = Column(String(45))

    Additive = relationship(u'Additive')
    Buffer = relationship(u'Buffer')
    MeasurementUnit = relationship(u'MeasurementUnit')


class CTF(Base):
    __tablename__ = 'CTF'

    ctfId = Column(Integer, primary_key=True)
    motionCorrectionId = Column(ForeignKey(u'MotionCorrection.motionCorrectionId'), index=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId'), index=True)
    boxSizeX = Column(Float)
    boxSizeY = Column(Float)
    minResolution = Column(Float)
    maxResolution = Column(Float)
    minDefocus = Column(Float)
    maxDefocus = Column(Float)
    defocusStepSize = Column(Float)
    astigmatism = Column(Float)
    astigmatismAngle = Column(Float)
    estimatedResolution = Column(Float)
    estimatedDefocus = Column(Float)
    amplitudeContrast = Column(Float)
    ccValue = Column(Float)
    fftTheoreticalFullPath = Column(String(255))
    comments = Column(String(255))

    AutoProcProgram = relationship(u'AutoProcProgram')
    MotionCorrection = relationship(u'MotionCorrection')


class CalendarHash(Base):
    __tablename__ = 'CalendarHash'

    calendarHashId = Column(Integer, primary_key=True)
    ckey = Column(String(50))
    hash = Column(String(128))
    beamline = Column(Integer)


class ComponentLattice(Base):
    __tablename__ = 'ComponentLattice'

    componentLatticeId = Column(Integer, primary_key=True)
    componentId = Column(ForeignKey(u'Protein.proteinId'), index=True)
    spaceGroup = Column(String(20))
    cell_a = Column(Float(asdecimal=True))
    cell_b = Column(Float(asdecimal=True))
    cell_c = Column(Float(asdecimal=True))
    cell_alpha = Column(Float(asdecimal=True))
    cell_beta = Column(Float(asdecimal=True))
    cell_gamma = Column(Float(asdecimal=True))

    Protein = relationship(u'Protein')


class ComponentSubType(Base):
    __tablename__ = 'ComponentSubType'

    componentSubTypeId = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)
    hasPh = Column(Integer, server_default=text("'0'"))


class ComponentType(Base):
    __tablename__ = 'ComponentType'

    componentTypeId = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)


t_Component_has_SubType = Table(
    'Component_has_SubType', Base.metadata,
    Column('componentId', ForeignKey(u'Protein.proteinId', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    Column('componentSubTypeId', ForeignKey(u'ComponentSubType.componentSubTypeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


class ConcentrationType(Base):
    __tablename__ = 'ConcentrationType'

    concentrationTypeId = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False)
    symbol = Column(String(8), nullable=False)


class Container(Base):
    __tablename__ = 'Container'

    containerId = Column(Integer, primary_key=True)
    dewarId = Column(ForeignKey(u'Dewar.dewarId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    code = Column(String(45))
    containerType = Column(String(20))
    capacity = Column(Integer)
    sampleChangerLocation = Column(String(20))
    containerStatus = Column(String(45), index=True)
    bltimeStamp = Column(DateTime)
    beamlineLocation = Column(String(20), index=True)
    screenId = Column(ForeignKey(u'Screen.screenId'), index=True)
    scheduleId = Column(ForeignKey(u'Schedule.scheduleId'), index=True)
    barcode = Column(String(45), unique=True)
    imagerId = Column(ForeignKey(u'Imager.imagerId'), index=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'SET NULL', onupdate=u'CASCADE'), index=True)
    ownerId = Column(ForeignKey(u'Person.personId'), index=True)
    requestedImagerId = Column(ForeignKey(u'Imager.imagerId'), index=True)
    requestedReturn = Column(Integer, server_default=text("'0'"))
    comments = Column(String(255))
    experimentType = Column(String(20))
    storageTemperature = Column(Float)
    containerRegistryId = Column(ForeignKey(u'ContainerRegistry.containerRegistryId'), index=True)

    ContainerRegistry = relationship(u'ContainerRegistry')
    Dewar = relationship(u'Dewar')
    Imager = relationship(u'Imager', primaryjoin='Container.imagerId == Imager.imagerId')
    Person = relationship(u'Person')
    Imager1 = relationship(u'Imager', primaryjoin='Container.requestedImagerId == Imager.imagerId')
    Schedule = relationship(u'Schedule')
    Screen = relationship(u'Screen')
    BLSession = relationship(u'BLSession')


class ContainerHistory(Base):
    __tablename__ = 'ContainerHistory'

    containerHistoryId = Column(Integer, primary_key=True)
    containerId = Column(ForeignKey(u'Container.containerId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    location = Column(String(45))
    blTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String(45))
    beamlineName = Column(String(20))

    Container = relationship(u'Container')


class ContainerInspection(Base):
    __tablename__ = 'ContainerInspection'

    containerInspectionId = Column(Integer, primary_key=True)
    containerId = Column(ForeignKey(u'Container.containerId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    inspectionTypeId = Column(ForeignKey(u'InspectionType.inspectionTypeId'), nullable=False, index=True)
    imagerId = Column(ForeignKey(u'Imager.imagerId'), index=True)
    temperature = Column(Float)
    blTimeStamp = Column(DateTime)
    scheduleComponentid = Column(ForeignKey(u'ScheduleComponent.scheduleComponentId'), index=True)
    state = Column(String(20))
    priority = Column(SmallInteger)
    manual = Column(Integer)
    scheduledTimeStamp = Column(DateTime)
    completedTimeStamp = Column(DateTime)

    Container = relationship(u'Container')
    Imager = relationship(u'Imager')
    InspectionType = relationship(u'InspectionType')
    ScheduleComponent = relationship(u'ScheduleComponent')


class ContainerQueue(Base):
    __tablename__ = 'ContainerQueue'

    containerQueueId = Column(Integer, primary_key=True)
    containerId = Column(ForeignKey(u'Container.containerId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    personId = Column(ForeignKey(u'Person.personId', onupdate=u'CASCADE'), index=True)
    createdTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    completedTimeStamp = Column(DateTime)

    Container = relationship(u'Container')
    Person = relationship(u'Person')


class ContainerQueueSample(Base):
    __tablename__ = 'ContainerQueueSample'

    containerQueueSampleId = Column(Integer, primary_key=True)
    containerQueueId = Column(ForeignKey(u'ContainerQueue.containerQueueId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)

    BLSubSample = relationship(u'BLSubSample')
    ContainerQueue = relationship(u'ContainerQueue')


class ContainerRegistry(Base):
    __tablename__ = 'ContainerRegistry'

    containerRegistryId = Column(Integer, primary_key=True)
    barcode = Column(String(20))
    comments = Column(String(255))
    recordTimestamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class ContainerRegistryHasProposal(Base):
    __tablename__ = 'ContainerRegistry_has_Proposal'
    __table_args__ = (
        Index('containerRegistryId', 'containerRegistryId', 'proposalId', unique=True),
    )

    containerRegistryHasProposalId = Column(Integer, primary_key=True)
    containerRegistryId = Column(ForeignKey(u'ContainerRegistry.containerRegistryId'))
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), index=True)
    personId = Column(ForeignKey(u'Person.personId'), index=True)
    recordTimestamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    ContainerRegistry = relationship(u'ContainerRegistry')
    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')


class ContainerReport(Base):
    __tablename__ = 'ContainerReport'

    containerReportId = Column(Integer, primary_key=True)
    containerRegistryId = Column(ForeignKey(u'ContainerRegistry.containerRegistryId'), index=True)
    personId = Column(ForeignKey(u'Person.personId'), index=True)
    report = Column(Text)
    attachmentFilePath = Column(String(255))
    recordTimestamp = Column(DateTime)

    ContainerRegistry = relationship(u'ContainerRegistry')
    Person = relationship(u'Person')


class CourierTermsAccepted(Base):
    __tablename__ = 'CourierTermsAccepted'

    courierTermsAcceptedId = Column(Integer, primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), nullable=False, index=True)
    personId = Column(ForeignKey(u'Person.personId'), nullable=False, index=True)
    shippingName = Column(String(100))
    timestamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    shippingId = Column(ForeignKey(u'Shipping.shippingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')
    Shipping = relationship(u'Shipping')


class Crystal(Base):
    __tablename__ = 'Crystal'

    crystalId = Column(Integer, primary_key=True)
    diffractionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    proteinId = Column(ForeignKey(u'Protein.proteinId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    crystalUUID = Column(String(45))
    name = Column(String(255))
    spaceGroup = Column(String(20))
    morphology = Column(String(255))
    color = Column(String(45))
    size_X = Column(Float(asdecimal=True))
    size_Y = Column(Float(asdecimal=True))
    size_Z = Column(Float(asdecimal=True))
    cell_a = Column(Float(asdecimal=True))
    cell_b = Column(Float(asdecimal=True))
    cell_c = Column(Float(asdecimal=True))
    cell_alpha = Column(Float(asdecimal=True))
    cell_beta = Column(Float(asdecimal=True))
    cell_gamma = Column(Float(asdecimal=True))
    comments = Column(String(255))
    pdbFileName = Column(String(255))
    pdbFilePath = Column(String(1024))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    abundance = Column(Float)
    theoreticalDensity = Column(Float)

    DiffractionPlan = relationship(u'DiffractionPlan')
    Protein = relationship(u'Protein')


class CrystalHasUUID(Base):
    __tablename__ = 'Crystal_has_UUID'

    crystal_has_UUID_Id = Column(Integer, primary_key=True)
    crystalId = Column(ForeignKey(u'Crystal.crystalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    UUID = Column(String(45), index=True)
    imageURL = Column(String(255))

    Crystal = relationship(u'Crystal')


class DataAcquisition(Base):
    __tablename__ = 'DataAcquisition'

    dataAcquisitionId = Column(Integer, primary_key=True)
    sampleCellId = Column(Integer, nullable=False)
    framesCount = Column(String(45))
    energy = Column(String(45))
    waitTime = Column(String(45))
    detectorDistance = Column(String(45))


class DataCollection(Base):
    __tablename__ = 'DataCollection'

    dataCollectionId = Column(Integer, primary_key=True)
    BLSAMPLEID = Column(Integer, index=True)
    SESSIONID = Column(Integer, index=True, server_default=text("'0'"))
    experimenttype = Column(String(24))
    dataCollectionNumber = Column(Integer, index=True)
    startTime = Column(DateTime, index=True)
    endTime = Column(DateTime)
    runStatus = Column(String(45))
    axisStart = Column(Float)
    axisEnd = Column(Float)
    axisRange = Column(Float)
    overlap = Column(Float)
    numberOfImages = Column(Integer)
    startImageNumber = Column(Integer)
    numberOfPasses = Column(Integer)
    exposureTime = Column(Float)
    imageDirectory = Column(String(255), index=True)
    imagePrefix = Column(String(45), index=True)
    imageSuffix = Column(String(45))
    imageContainerSubPath = Column(String(255))
    fileTemplate = Column(String(255))
    wavelength = Column(Float)
    resolution = Column(Float)
    detectorDistance = Column(Float)
    xBeam = Column(Float)
    yBeam = Column(Float)
    comments = Column(String(1024))
    printableForReport = Column(Integer, server_default=text("'1'"))
    CRYSTALCLASS = Column(String(20))
    slitGapVertical = Column(Float)
    slitGapHorizontal = Column(Float)
    transmission = Column(Float)
    synchrotronMode = Column(String(20))
    xtalSnapshotFullPath1 = Column(String(255))
    xtalSnapshotFullPath2 = Column(String(255))
    xtalSnapshotFullPath3 = Column(String(255))
    xtalSnapshotFullPath4 = Column(String(255))
    rotationAxis = Column(ENUM(u'Omega', u'Kappa', u'Phi'))
    phiStart = Column(Float)
    kappaStart = Column(Float)
    omegaStart = Column(Float)
    chiStart = Column(Float)
    resolutionAtCorner = Column(Float)
    detector2Theta = Column(Float)
    DETECTORMODE = Column(String(255))
    undulatorGap1 = Column(Float)
    undulatorGap2 = Column(Float)
    undulatorGap3 = Column(Float)
    beamSizeAtSampleX = Column(Float)
    beamSizeAtSampleY = Column(Float)
    centeringMethod = Column(String(255))
    averageTemperature = Column(Float)
    ACTUALSAMPLEBARCODE = Column(String(45))
    ACTUALSAMPLESLOTINCONTAINER = Column(Integer)
    ACTUALCONTAINERBARCODE = Column(String(45))
    ACTUALCONTAINERSLOTINSC = Column(Integer)
    actualCenteringPosition = Column(String(255))
    beamShape = Column(String(45))
    dataCollectionGroupId = Column(ForeignKey(u'DataCollectionGroup.dataCollectionGroupId'), nullable=False, index=True)
    POSITIONID = Column(Integer)
    detectorId = Column(ForeignKey(u'Detector.detectorId'), index=True)
    FOCALSPOTSIZEATSAMPLEX = Column(Float)
    POLARISATION = Column(Float)
    FOCALSPOTSIZEATSAMPLEY = Column(Float)
    APERTUREID = Column(Integer)
    screeningOrigId = Column(Integer)
    startPositionId = Column(ForeignKey(u'MotorPosition.motorPositionId'), index=True)
    endPositionId = Column(ForeignKey(u'MotorPosition.motorPositionId'), index=True)
    flux = Column(Float(asdecimal=True))
    strategySubWedgeOrigId = Column(ForeignKey(u'ScreeningStrategySubWedge.screeningStrategySubWedgeId'), index=True)
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId'), index=True)
    flux_end = Column(Float(asdecimal=True))
    bestWilsonPlotPath = Column(String(255))
    processedDataFile = Column(String(255))
    datFullPath = Column(String(255))
    magnification = Column(Float)
    totalAbsorbedDose = Column(Float)
    binning = Column(Integer, server_default=text("'1'"))
    particleDiameter = Column(Float)
    boxSize_CTF = Column(Float)
    minResolution = Column(Float)
    minDefocus = Column(Float)
    maxDefocus = Column(Float)
    defocusStepSize = Column(Float)
    amountAstigmatism = Column(Float)
    extractSize = Column(Float)
    bgRadius = Column(Float)
    voltage = Column(Float)
    objAperture = Column(Float)
    c1aperture = Column(Float)
    c2aperture = Column(Float)
    c3aperture = Column(Float)
    c1lens = Column(Float)
    c2lens = Column(Float)
    c3lens = Column(Float)
    totalExposedDose = Column(Float)
    nominalMagnification = Column(Float)
    nominalDefocus = Column(Float)
    imageSizeX = Column(Integer)
    imageSizeY = Column(Integer)
    pixelSizeOnImage = Column(Float)
    phasePlate = Column(Integer)

    BLSubSample = relationship(u'BLSubSample')
    DataCollectionGroup = relationship(u'DataCollectionGroup')
    Detector = relationship(u'Detector')
    MotorPosition = relationship(u'MotorPosition', primaryjoin='DataCollection.endPositionId == MotorPosition.motorPositionId')
    MotorPosition1 = relationship(u'MotorPosition', primaryjoin='DataCollection.startPositionId == MotorPosition.motorPositionId')
    ScreeningStrategySubWedge = relationship(u'ScreeningStrategySubWedge')


class DataCollectionComment(Base):
    __tablename__ = 'DataCollectionComment'

    dataCollectionCommentId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    comments = Column(String(4000))
    createTime = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modTime = Column(Date)

    DataCollection = relationship(u'DataCollection')
    Person = relationship(u'Person')


class DataCollectionFileAttachment(Base):
    __tablename__ = 'DataCollectionFileAttachment'

    dataCollectionFileAttachmentId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    fileFullPath = Column(String(255), nullable=False)
    fileType = Column(ENUM(u'snapshot', u'log', u'xy', u'recip', u'pia', u'warning'))
    createTime = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    DataCollection = relationship(u'DataCollection')


class DataCollectionGroup(Base):
    __tablename__ = 'DataCollectionGroup'

    dataCollectionGroupId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    comments = Column(String(1024))
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    experimentType = Column(ENUM(u'SAD', u'SAD - Inverse Beam', u'OSC', u'Collect - Multiwedge', u'MAD', u'Helical', u'Multi-positional', u'Mesh', u'Burn', u'MAD - Inverse Beam', u'Characterization', u'Dehydration', u'tomo', u'experiment', u'EM', u'PDF', u'PDF+Bragg', u'Bragg', u'single particle', u'Serial Fixed', u'Serial Jet'))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    crystalClass = Column(String(20))
    detectorMode = Column(String(255))
    actualSampleBarcode = Column(String(45))
    actualSampleSlotInContainer = Column(Integer)
    actualContainerBarcode = Column(String(45))
    actualContainerSlotInSC = Column(Integer)
    workflowId = Column(ForeignKey(u'Workflow.workflowId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    xtalSnapshotFullPath = Column(String(255))

    BLSample = relationship(u'BLSample')
    BLSession = relationship(u'BLSession')
    Workflow = relationship(u'Workflow')
    Project = relationship(u'Project', secondary='Project_has_DCGroup')


class DataCollectionPlanHasDetector(Base):
    __tablename__ = 'DataCollectionPlan_has_Detector'
    __table_args__ = (
        Index('dataCollectionPlanId', 'dataCollectionPlanId', 'detectorId', unique=True),
    )

    dataCollectionPlanHasDetectorId = Column(Integer, primary_key=True)
    dataCollectionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId'), nullable=False)
    detectorId = Column(ForeignKey(u'Detector.detectorId'), nullable=False, index=True)
    exposureTime = Column(Float(asdecimal=True))
    distance = Column(Float(asdecimal=True))
    roll = Column(Float(asdecimal=True))

    DiffractionPlan = relationship(u'DiffractionPlan')
    Detector = relationship(u'Detector')


class DataReductionStatu(Base):
    __tablename__ = 'DataReductionStatus'

    dataReductionStatusId = Column(Integer, primary_key=True)
    dataCollectionId = Column(Integer, nullable=False)
    status = Column(String(15))
    filename = Column(String(255))
    message = Column(String(255))


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


class Dewar(Base):
    __tablename__ = 'Dewar'

    dewarId = Column(Integer, primary_key=True)
    shippingId = Column(ForeignKey(u'Shipping.shippingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    code = Column(String(45), index=True)
    comments = Column(String)
    storageLocation = Column(String(45))
    dewarStatus = Column(String(45), index=True)
    bltimeStamp = Column(DateTime)
    isStorageDewar = Column(Integer, server_default=text("'0'"))
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


class DewarLocation(Base):
    __tablename__ = 'DewarLocation'

    eventId = Column(Integer, primary_key=True)
    dewarNumber = Column(String(128), nullable=False)
    userId = Column(String(128))
    dateTime = Column(DateTime)
    locationName = Column(String(128))
    courierName = Column(String(128))
    courierTrackingNumber = Column(String(128))


class DewarLocationList(Base):
    __tablename__ = 'DewarLocationList'

    locationId = Column(Integer, primary_key=True)
    locationName = Column(String(128), nullable=False, server_default=text("''"))


class DewarRegistry(Base):
    __tablename__ = 'DewarRegistry'

    facilityCode = Column(String(20), primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId', ondelete=u'CASCADE'), nullable=False, index=True)
    labContactId = Column(ForeignKey(u'LabContact.labContactId', ondelete=u'CASCADE'), nullable=False, index=True)
    purchaseDate = Column(DateTime)
    bltimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    LabContact = relationship(u'LabContact')
    Proposal = relationship(u'Proposal')


class DewarReport(Base):
    __tablename__ = 'DewarReport'

    dewarReportId = Column(Integer, primary_key=True)
    facilityCode = Column(ForeignKey(u'DewarRegistry.facilityCode', ondelete=u'CASCADE'), nullable=False, index=True)
    report = Column(Text)
    attachment = Column(String(255))
    bltimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    DewarRegistry = relationship(u'DewarRegistry')


class DewarTransportHistory(Base):
    __tablename__ = 'DewarTransportHistory'

    DewarTransportHistoryId = Column(Integer, primary_key=True)
    dewarId = Column(ForeignKey(u'Dewar.dewarId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    dewarStatus = Column(String(45), nullable=False)
    storageLocation = Column(String(45), nullable=False)
    arrivalDate = Column(DateTime, nullable=False)

    Dewar = relationship(u'Dewar')


class DiffractionPlan(Base):
    __tablename__ = 'DiffractionPlan'

    diffractionPlanId = Column(Integer, primary_key=True)
    name = Column(String(20))
    experimentKind = Column(ENUM(u'Default', u'MXPressE', u'MXPressO', u'MXPressE_SAD', u'MXScore', u'MXPressM', u'MAD', u'SAD', u'Fixed', u'Ligand binding', u'Refinement', u'OSC', u'MAD - Inverse Beam', u'SAD - Inverse Beam', u'MESH', u'XFE'))
    observedResolution = Column(Float)
    minimalResolution = Column(Float)
    exposureTime = Column(Float)
    oscillationRange = Column(Float)
    maximalResolution = Column(Float)
    screeningResolution = Column(Float)
    radiationSensitivity = Column(Float)
    anomalousScatterer = Column(String(255))
    preferredBeamSizeX = Column(Float)
    preferredBeamSizeY = Column(Float)
    preferredBeamDiameter = Column(Float)
    comments = Column(String(1024))
    DIFFRACTIONPLANUUID = Column(String(1000))
    aimedCompleteness = Column(Float(asdecimal=True))
    aimedIOverSigmaAtHighestRes = Column(Float(asdecimal=True))
    aimedMultiplicity = Column(Float(asdecimal=True))
    aimedResolution = Column(Float(asdecimal=True))
    anomalousData = Column(Integer, server_default=text("'0'"))
    complexity = Column(String(45))
    estimateRadiationDamage = Column(Integer, server_default=text("'0'"))
    forcedSpaceGroup = Column(String(45))
    requiredCompleteness = Column(Float(asdecimal=True))
    requiredMultiplicity = Column(Float(asdecimal=True))
    requiredResolution = Column(Float(asdecimal=True))
    strategyOption = Column(String(45))
    kappaStrategyOption = Column(String(45))
    numberOfPositions = Column(Integer)
    minDimAccrossSpindleAxis = Column(Float(asdecimal=True))
    maxDimAccrossSpindleAxis = Column(Float(asdecimal=True))
    radiationSensitivityBeta = Column(Float(asdecimal=True))
    radiationSensitivityGamma = Column(Float(asdecimal=True))
    minOscWidth = Column(Float)
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    monochromator = Column(String(8))
    energy = Column(Float)
    transmission = Column(Float)
    boxSizeX = Column(Float)
    boxSizeY = Column(Float)
    kappaStart = Column(Float)
    axisStart = Column(Float)
    axisRange = Column(Float)
    numberOfImages = Column(Integer)
    presetForProposalId = Column(ForeignKey(u'Proposal.proposalId'), index=True)
    beamLineName = Column(String(45))
    detectorId = Column(ForeignKey(u'Detector.detectorId', onupdate=u'CASCADE'), index=True)
    distance = Column(Float(asdecimal=True))
    orientation = Column(Float(asdecimal=True))
    monoBandwidth = Column(Float(asdecimal=True))

    Detector = relationship(u'Detector')
    Proposal = relationship(u'Proposal')


class EMMicroscope(Base):
    __tablename__ = 'EMMicroscope'

    emMicroscopeId = Column(Integer, primary_key=True)
    instrumentName = Column(String(100), nullable=False)
    voltage = Column(Float)
    CS = Column(Float)
    detectorPixelSize = Column(Float)
    C2aperture = Column(Float)
    ObjAperture = Column(Float)
    C2lens = Column(Float)


class EnergyScan(Base):
    __tablename__ = 'EnergyScan'

    energyScanId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId'), index=True)
    fluorescenceDetector = Column(String(255))
    scanFileFullPath = Column(String(255))
    jpegChoochFileFullPath = Column(String(255))
    element = Column(String(45))
    startEnergy = Column(Float)
    endEnergy = Column(Float)
    transmissionFactor = Column(Float)
    exposureTime = Column(Float)
    synchrotronCurrent = Column(Float)
    temperature = Column(Float)
    peakEnergy = Column(Float)
    peakFPrime = Column(Float)
    peakFDoublePrime = Column(Float)
    inflectionEnergy = Column(Float)
    inflectionFPrime = Column(Float)
    inflectionFDoublePrime = Column(Float)
    xrayDose = Column(Float)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    edgeEnergy = Column(String(255))
    filename = Column(String(255))
    beamSizeVertical = Column(Float)
    beamSizeHorizontal = Column(Float)
    choochFileFullPath = Column(String(255))
    crystalClass = Column(String(20))
    comments = Column(String(1024))
    flux = Column(Float(asdecimal=True))
    flux_end = Column(Float(asdecimal=True))
    workingDirectory = Column(String(45))
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId'), index=True)

    BLSample = relationship(u'BLSample')
    BLSubSample = relationship(u'BLSubSample')
    BLSession = relationship(u'BLSession')
    Project = relationship(u'Project', secondary='Project_has_EnergyScan')


class Experiment(Base):
    __tablename__ = 'Experiment'

    experimentId = Column(Integer, primary_key=True)
    proposalId = Column(Integer, nullable=False)
    name = Column(String(255))
    creationDate = Column(DateTime)
    comments = Column(String(512))
    experimentType = Column(String(128))
    sourceFilePath = Column(String(256))
    dataAcquisitionFilePath = Column(String(256))
    status = Column(String(45))
    sessionId = Column(Integer)


class ExperimentKindDetail(Base):
    __tablename__ = 'ExperimentKindDetails'

    experimentKindId = Column(Integer, primary_key=True)
    diffractionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    exposureIndex = Column(Integer)
    dataCollectionType = Column(String(45))
    dataCollectionKind = Column(String(45))
    wedgeValue = Column(Float)

    DiffractionPlan = relationship(u'DiffractionPlan')


class Frame(Base):
    __tablename__ = 'Frame'

    frameId = Column(Integer, primary_key=True)
    FRAMESETID = Column(Integer)
    filePath = Column(String(255))
    comments = Column(String(45))


class FrameList(Base):
    __tablename__ = 'FrameList'

    frameListId = Column(Integer, primary_key=True)
    comments = Column(Integer)


class FrameSet(Base):
    __tablename__ = 'FrameSet'

    frameSetId = Column(Integer, primary_key=True)
    runId = Column(ForeignKey(u'Run.runId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    FILEPATH = Column(String(255))
    INTERNALPATH = Column(String(255))
    frameListId = Column(ForeignKey(u'FrameList.frameListId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    detectorId = Column(Integer)
    detectorDistance = Column(String(45))

    FrameList = relationship(u'FrameList')
    Run = relationship(u'Run')


class FrameToList(Base):
    __tablename__ = 'FrameToList'

    frameToListId = Column(Integer, primary_key=True)
    frameListId = Column(ForeignKey(u'FrameList.frameListId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    frameId = Column(ForeignKey(u'Frame.frameId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    Frame = relationship(u'Frame')
    FrameList = relationship(u'FrameList')


class GeometryClassname(Base):
    __tablename__ = 'GeometryClassname'

    geometryClassnameId = Column(Integer, primary_key=True)
    geometryClassname = Column(String(45))
    geometryOrder = Column(Integer, nullable=False)


class GridImageMap(Base):
    __tablename__ = 'GridImageMap'

    gridImageMapId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    imageNumber = Column(Integer)
    outputFileId = Column(String(80))
    positionX = Column(Float)
    positionY = Column(Float)

    DataCollection = relationship(u'DataCollection')


class GridInfo(Base):
    __tablename__ = 'GridInfo'

    gridInfoId = Column(Integer, primary_key=True)
    xOffset = Column(Float(asdecimal=True))
    yOffset = Column(Float(asdecimal=True))
    dx_mm = Column(Float(asdecimal=True))
    dy_mm = Column(Float(asdecimal=True))
    steps_x = Column(Float(asdecimal=True))
    steps_y = Column(Float(asdecimal=True))
    meshAngle = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    workflowMeshId = Column(ForeignKey(u'WorkflowMesh.workflowMeshId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    orientation = Column(ENUM(u'vertical', u'horizontal'), server_default=text("'horizontal'"))
    dataCollectionGroupId = Column(ForeignKey(u'DataCollectionGroup.dataCollectionGroupId'), index=True)
    pixelsPerMicronX = Column(Float)
    pixelsPerMicronY = Column(Float)
    snapshot_offsetXPixel = Column(Float)
    snapshot_offsetYPixel = Column(Float)
    snaked = Column(Integer, server_default=text("'0'"))

    DataCollectionGroup = relationship(u'DataCollectionGroup')
    WorkflowMesh = relationship(u'WorkflowMesh')


class Image(Base):
    __tablename__ = 'Image'
    __table_args__ = (
        Index('Image_Index3', 'fileLocation', 'fileName'),
    )

    imageId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    imageNumber = Column(Integer, index=True)
    fileName = Column(String(255))
    fileLocation = Column(String(255))
    measuredIntensity = Column(Float)
    jpegFileFullPath = Column(String(255))
    jpegThumbnailFileFullPath = Column(String(255))
    temperature = Column(Float)
    cumulativeIntensity = Column(Float)
    synchrotronCurrent = Column(Float)
    comments = Column(String(1024))
    machineMessage = Column(String(1024))
    BLTIMESTAMP = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    motorPositionId = Column(ForeignKey(u'MotorPosition.motorPositionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    DataCollection = relationship(u'DataCollection')
    MotorPosition = relationship(u'MotorPosition')


class ImageQualityIndicator(Base):
    __tablename__ = 'ImageQualityIndicators'

    dataCollectionId = Column(Integer, primary_key=True, nullable=False)
    imageNumber = Column(Integer, primary_key=True, nullable=False)
    imageId = Column(Integer)
    autoProcProgramId = Column(Integer)
    spotTotal = Column(Integer)
    inResTotal = Column(Integer)
    goodBraggCandidates = Column(Integer)
    iceRings = Column(Integer)
    method1Res = Column(Float)
    method2Res = Column(Float)
    maxUnitCell = Column(Float)
    pctSaturationTop50Peaks = Column(Float)
    inResolutionOvrlSpots = Column(Integer)
    binPopCutOffMethod2Res = Column(Float)
    recordTimeStamp = Column(DateTime)
    totalIntegratedSignal = Column(Float(asdecimal=True))
    dozor_score = Column(Float(asdecimal=True))
    driftFactor = Column(Float)


class Imager(Base):
    __tablename__ = 'Imager'

    imagerId = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    temperature = Column(Float)
    serial = Column(String(45))
    capacity = Column(SmallInteger)


class InspectionType(Base):
    __tablename__ = 'InspectionType'

    inspectionTypeId = Column(Integer, primary_key=True)
    name = Column(String(45))


class Instruction(Base):
    __tablename__ = 'Instruction'

    instructionId = Column(Integer, primary_key=True)
    instructionSetId = Column(ForeignKey(u'InstructionSet.instructionSetId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    INSTRUCTIONORDER = Column(Integer)
    comments = Column(String(255))
    order = Column(Integer, nullable=False)

    InstructionSet = relationship(u'InstructionSet')


class InstructionSet(Base):
    __tablename__ = 'InstructionSet'

    instructionSetId = Column(Integer, primary_key=True)
    type = Column(String(50))


class IspybCrystalClas(Base):
    __tablename__ = 'IspybCrystalClass'

    crystalClassId = Column(Integer, primary_key=True)
    crystalClass_code = Column(String(20), nullable=False)
    crystalClass_name = Column(String(255), nullable=False)


class IspybReference(Base):
    __tablename__ = 'IspybReference'

    referenceId = Column(Integer, primary_key=True)
    referenceName = Column(String(255))
    referenceUrl = Column(String(1024))
    referenceBibtext = Column(LargeBinary)
    beamline = Column(ENUM(u'All', u'ID14-4', u'ID23-1', u'ID23-2', u'ID29', u'XRF', u'AllXRF', u'Mesh'))


class LabContact(Base):
    __tablename__ = 'LabContact'
    __table_args__ = (
        Index('cardNameAndProposal', 'cardName', 'proposalId', unique=True),
        Index('personAndProposal', 'personId', 'proposalId', unique=True)
    )

    labContactId = Column(Integer, primary_key=True)
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    cardName = Column(String(40), nullable=False)
    proposalId = Column(ForeignKey(u'Proposal.proposalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    defaultCourrierCompany = Column(String(45))
    courierAccount = Column(String(45))
    billingReference = Column(String(45))
    dewarAvgCustomsValue = Column(Integer, nullable=False, server_default=text("'0'"))
    dewarAvgTransportValue = Column(Integer, nullable=False, server_default=text("'0'"))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

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
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
#    laboratoryPk = Column(Integer)
    postcode = Column(String(15))


class Log4Stat(Base):
    __tablename__ = 'Log4Stat'

    id = Column(Integer, primary_key=True)
    priority = Column(String(15))
    LOG4JTIMESTAMP = Column(DateTime)
    msg = Column(String(255))
    detail = Column(String(255))
    value = Column(String(255))
    timestamp = Column(DateTime)


class MXMRRun(Base):
    __tablename__ = 'MXMRRun'

    mxMRRunId = Column(Integer, primary_key=True)
    autoProcScalingId = Column(ForeignKey(u'AutoProcScaling.autoProcScalingId'), nullable=False, index=True)
    success = Column(Integer, server_default=text("'0'"))
    message = Column(String(255))
    pipeline = Column(String(50))
    inputCoordFile = Column(String(255))
    outputCoordFile = Column(String(255))
    inputMTZFile = Column(String(255))
    outputMTZFile = Column(String(255))
    runDirectory = Column(String(255))
    logFile = Column(String(255))
    commandLine = Column(String(255))
    rValueStart = Column(Float)
    rValueEnd = Column(Float)
    rFreeValueStart = Column(Float)
    rFreeValueEnd = Column(Float)
    starttime = Column(DateTime)
    endtime = Column(DateTime)

    AutoProcScaling = relationship(u'AutoProcScaling')


class MXMRRunBlob(Base):
    __tablename__ = 'MXMRRunBlob'

    mxMRRunBlobId = Column(Integer, primary_key=True)
    mxMRRunId = Column(ForeignKey(u'MXMRRun.mxMRRunId'), nullable=False, index=True)
    view1 = Column(String(255))
    view2 = Column(String(255))
    view3 = Column(String(255))

    MXMRRun = relationship(u'MXMRRun')


class Macromolecule(Base):
    __tablename__ = 'Macromolecule'

    macromoleculeId = Column(Integer, primary_key=True)
    proposalId = Column(Integer)
    safetyLevelId = Column(ForeignKey(u'SafetyLevel.safetyLevelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    name = Column(String(45))
    acronym = Column(String(45))
    molecularMass = Column(String(45))
    extintionCoefficient = Column(String(45))
    sequence = Column(String(1000))
    creationDate = Column(DateTime)
    comments = Column(String(1024))

    SafetyLevel = relationship(u'SafetyLevel')


class MacromoleculeRegion(Base):
    __tablename__ = 'MacromoleculeRegion'

    macromoleculeRegionId = Column(Integer, primary_key=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    regionType = Column(String(45))
    id = Column(String(45))
    count = Column(String(45))
    sequence = Column(String(45))

    Macromolecule = relationship(u'Macromolecule')


class Measurement(Base):
    __tablename__ = 'Measurement'

    specimenId = Column(ForeignKey(u'Specimen.specimenId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    runId = Column(ForeignKey(u'Run.runId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    code = Column(String(100))
    priorityLevelId = Column(Integer)
    exposureTemperature = Column(String(45))
    viscosity = Column(String(45))
    flow = Column(Integer)
    extraFlowTime = Column(String(45))
    volumeToLoad = Column(String(45))
    waitTime = Column(String(45))
    transmission = Column(String(45))
    comments = Column(String(512))
    measurementId = Column(Integer, primary_key=True)

    Run = relationship(u'Run')
    Speciman = relationship('Speciman')


class MeasurementToDataCollection(Base):
    __tablename__ = 'MeasurementToDataCollection'

    measurementToDataCollectionId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'SaxsDataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    measurementId = Column(ForeignKey(u'Measurement.measurementId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    dataCollectionOrder = Column(Integer)

    SaxsDataCollection = relationship(u'SaxsDataCollection')
    Measurement = relationship(u'Measurement')


class MeasurementUnit(Base):
    __tablename__ = 'MeasurementUnit'

    measurementUnitId = Column(Integer, primary_key=True)
    name = Column(String(45))
    unitType = Column(String(45))


class Merge(Base):
    __tablename__ = 'Merge'

    mergeId = Column(Integer, primary_key=True)
    measurementId = Column(ForeignKey(u'Measurement.measurementId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    frameListId = Column(ForeignKey(u'FrameList.frameListId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    discardedFrameNameList = Column(String(1024))
    averageFilePath = Column(String(255))
    framesCount = Column(String(45))
    framesMerge = Column(String(45))

    FrameList = relationship(u'FrameList')
    Measurement = relationship(u'Measurement')


class Model(Base):
    __tablename__ = 'Model'

    modelId = Column(Integer, primary_key=True)
    name = Column(String(45))
    pdbFile = Column(String(255))
    fitFile = Column(String(255))
    firFile = Column(String(255))
    logFile = Column(String(255))
    rFactor = Column(String(45))
    chiSqrt = Column(String(45))
    volume = Column(String(45))
    rg = Column(String(45))
    dMax = Column(String(45))


class ModelBuilding(Base):
    __tablename__ = 'ModelBuilding'

    modelBuildingId = Column(Integer, primary_key=True)
    phasingAnalysisId = Column(ForeignKey(u'PhasingAnalysis.phasingAnalysisId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    phasingProgramRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    spaceGroupId = Column(ForeignKey(u'SpaceGroup.spaceGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime)

    PhasingAnalysi = relationship('PhasingAnalysi')
    PhasingProgramRun = relationship(u'PhasingProgramRun')
    SpaceGroup = relationship(u'SpaceGroup')


class ModelList(Base):
    __tablename__ = 'ModelList'

    modelListId = Column(Integer, primary_key=True)
    nsdFilePath = Column(String(255))
    chi2RgFilePath = Column(String(255))


class ModelToList(Base):
    __tablename__ = 'ModelToList'

    modelToListId = Column(Integer, primary_key=True)
    modelId = Column(ForeignKey(u'Model.modelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    modelListId = Column(ForeignKey(u'ModelList.modelListId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    Model = relationship(u'Model')
    ModelList = relationship(u'ModelList')


class MotionCorrection(Base):
    __tablename__ = 'MotionCorrection'

    motionCorrectionId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId'), index=True)
    imageNumber = Column(SmallInteger)
    firstFrame = Column(SmallInteger)
    lastFrame = Column(SmallInteger)
    dosePerFrame = Column(Float)
    doseWeight = Column(Float)
    totalMotion = Column(Float)
    averageMotionPerFrame = Column(Float)
    driftPlotFullPath = Column(String(255))
    micrographFullPath = Column(String(255))
    micrographSnapshotFullPath = Column(String(255))
    patchesUsedX = Column(Integer)
    patchesUsedY = Column(Integer)
    fftFullPath = Column(String(255))
    fftCorrectedFullPath = Column(String(255))
    comments = Column(String(255))
    movieId = Column(ForeignKey(u'Movie.movieId'), index=True)

    AutoProcProgram = relationship(u'AutoProcProgram')
    DataCollection = relationship(u'DataCollection')
    Movie = relationship(u'Movie')


class MotionCorrectionDrift(Base):
    __tablename__ = 'MotionCorrectionDrift'

    motionCorrectionDriftId = Column(Integer, primary_key=True)
    motionCorrectionId = Column(ForeignKey(u'MotionCorrection.motionCorrectionId'), index=True)
    frameNumber = Column(SmallInteger)
    deltaX = Column(Float)
    deltaY = Column(Float)

    MotionCorrection = relationship(u'MotionCorrection')


class MotorPosition(Base):
    __tablename__ = 'MotorPosition'

    motorPositionId = Column(Integer, primary_key=True)
    phiX = Column(Float(asdecimal=True))
    phiY = Column(Float(asdecimal=True))
    phiZ = Column(Float(asdecimal=True))
    sampX = Column(Float(asdecimal=True))
    sampY = Column(Float(asdecimal=True))
    omega = Column(Float(asdecimal=True))
    kappa = Column(Float(asdecimal=True))
    phi = Column(Float(asdecimal=True))
    chi = Column(Float(asdecimal=True))
    gridIndexY = Column(Integer)
    gridIndexZ = Column(Integer)
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Movie(Base):
    __tablename__ = 'Movie'

    movieId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    movieNumber = Column(Integer)
    movieFullPath = Column(String(255))
    createdTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    positionX = Column(Float)
    positionY = Column(Float)
    nominalDefocus = Column(Float)

    DataCollection = relationship(u'DataCollection')


class PDB(Base):
    __tablename__ = 'PDB'

    pdbId = Column(Integer, primary_key=True)
    name = Column(String(255))
    contents = Column(String)
    code = Column(String(4))


class PDBEntry(Base):
    __tablename__ = 'PDBEntry'

    pdbEntryId = Column(Integer, primary_key=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId', ondelete=u'CASCADE'), nullable=False, index=True)
    code = Column(String(4))
    cell_a = Column(Float)
    cell_b = Column(Float)
    cell_c = Column(Float)
    cell_alpha = Column(Float)
    cell_beta = Column(Float)
    cell_gamma = Column(Float)
    resolution = Column(Float)
    pdbTitle = Column(String(255))
    pdbAuthors = Column(String(600))
    pdbDate = Column(DateTime)
    pdbBeamlineName = Column(String(50))
    beamlines = Column(String(100))
    distance = Column(Float)
    autoProcCount = Column(SmallInteger)
    dataCollectionCount = Column(SmallInteger)
    beamlineMatch = Column(Integer)
    authorMatch = Column(Integer)

    AutoProcProgram = relationship(u'AutoProcProgram')


class PDBEntryHasAutoProcProgram(Base):
    __tablename__ = 'PDBEntry_has_AutoProcProgram'

    pdbEntryHasAutoProcId = Column(Integer, primary_key=True)
    pdbEntryId = Column(ForeignKey(u'PDBEntry.pdbEntryId', ondelete=u'CASCADE'), nullable=False, index=True)
    autoProcProgramId = Column(ForeignKey(u'AutoProcProgram.autoProcProgramId', ondelete=u'CASCADE'), nullable=False, index=True)
    distance = Column(Float)

    AutoProcProgram = relationship(u'AutoProcProgram')
    PDBEntry = relationship(u'PDBEntry')


class PHPSession(Base):
    __tablename__ = 'PHPSession'

    id = Column(String(50), primary_key=True)
    accessDate = Column(DateTime)
    data = Column(String(4000))


class Particle(Base):
    __tablename__ = 'Particle'

    particleId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    x = Column(Float)
    y = Column(Float)

    DataCollection = relationship(u'DataCollection')


class Permission(Base):
    __tablename__ = 'Permission'

    permissionId = Column(Integer, primary_key=True)
    type = Column(String(15), nullable=False)
    description = Column(String(100))

    UserGroup = relationship(u'UserGroup', secondary='UserGroup_has_Permission')


class Person(Base):
    __tablename__ = 'Person'

    personId = Column(Integer, primary_key=True)
    laboratoryId = Column(ForeignKey(u'Laboratory.laboratoryId'), index=True)
    siteId = Column(Integer, index=True)
    personUUID = Column(String(45))
    familyName = Column(String(100), index=True)
    givenName = Column(String(45))
    title = Column(String(45))
    emailAddress = Column(String(60))
    phoneNumber = Column(String(45))
    login = Column(String(45), unique=True)
    faxNumber = Column(String(45))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    cache = Column(Text)
    externalId = Column(BINARY(16))

    Laboratory = relationship(u'Laboratory')
    UserGroup = relationship(u'UserGroup', secondary='UserGroup_has_Person')
    Project = relationship(u'Project', secondary='Project_has_Person')

    def __str__(self):
        return "{}, {}: {}".format(self.familyName, self.givenName, self.login)

class Phasing(Base):
    __tablename__ = 'Phasing'

    phasingId = Column(Integer, primary_key=True)
    phasingAnalysisId = Column(ForeignKey(u'PhasingAnalysis.phasingAnalysisId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    phasingProgramRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    spaceGroupId = Column(ForeignKey(u'SpaceGroup.spaceGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    method = Column(ENUM(u'solvent flattening', u'solvent flipping'))
    solventContent = Column(Float(asdecimal=True))
    enantiomorph = Column(Integer)
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    PhasingAnalysi = relationship('PhasingAnalysi')
    PhasingProgramRun = relationship(u'PhasingProgramRun')
    SpaceGroup = relationship(u'SpaceGroup')


class PhasingAnalysi(Base):
    __tablename__ = 'PhasingAnalysis'

    phasingAnalysisId = Column(Integer, primary_key=True)
    recordTimeStamp = Column(DateTime)


class PhasingProgramAttachment(Base):
    __tablename__ = 'PhasingProgramAttachment'

    phasingProgramAttachmentId = Column(Integer, primary_key=True)
    phasingProgramRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    fileType = Column(ENUM(u'Map', u'Logfile', u'PDB', u'CSV', u'INS', u'RES', u'TXT'))
    fileName = Column(String(45))
    filePath = Column(String(255))
    recordTimeStamp = Column(DateTime)

    PhasingProgramRun = relationship(u'PhasingProgramRun')


class PhasingProgramRun(Base):
    __tablename__ = 'PhasingProgramRun'

    phasingProgramRunId = Column(Integer, primary_key=True)
    phasingCommandLine = Column(String(255))
    phasingPrograms = Column(String(255))
    phasingStatus = Column(Integer)
    phasingMessage = Column(String(255))
    phasingStartTime = Column(DateTime)
    phasingEndTime = Column(DateTime)
    phasingEnvironment = Column(String(255))
    recordTimeStamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class PhasingStatistic(Base):
    __tablename__ = 'PhasingStatistics'

    phasingStatisticsId = Column(Integer, primary_key=True)
    phasingHasScalingId1 = Column(ForeignKey(u'Phasing_has_Scaling.phasingHasScalingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    phasingHasScalingId2 = Column(ForeignKey(u'Phasing_has_Scaling.phasingHasScalingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    phasingStepId = Column(ForeignKey(u'PhasingStep.phasingStepId'), index=True)
    numberOfBins = Column(Integer)
    binNumber = Column(Integer)
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    metric = Column(ENUM(u'Rcullis', u'Average Fragment Length', u'Chain Count', u'Residues Count', u'CC', u'PhasingPower', u'FOM', u'<d"/sig>', u'Best CC', u'CC(1/2)', u'Weak CC', u'CFOM', u'Pseudo_free_CC', u'CC of partial model'))
    statisticsValue = Column(Float(asdecimal=True))
    nReflections = Column(Integer)
    recordTimeStamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    Phasing_has_Scaling = relationship(u'PhasingHasScaling', primaryjoin='PhasingStatistic.phasingHasScalingId1 == PhasingHasScaling.phasingHasScalingId')
    Phasing_has_Scaling1 = relationship(u'PhasingHasScaling', primaryjoin='PhasingStatistic.phasingHasScalingId2 == PhasingHasScaling.phasingHasScalingId')
    PhasingStep = relationship(u'PhasingStep')


class PhasingStep(Base):
    __tablename__ = 'PhasingStep'

    phasingStepId = Column(Integer, primary_key=True)
    previousPhasingStepId = Column(Integer)
    programRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId'), index=True)
    spaceGroupId = Column(ForeignKey(u'SpaceGroup.spaceGroupId'), index=True)
    autoProcScalingId = Column(ForeignKey(u'AutoProcScaling.autoProcScalingId'), index=True)
    phasingAnalysisId = Column(Integer, index=True)
    phasingStepType = Column(ENUM(u'PREPARE', u'SUBSTRUCTUREDETERMINATION', u'PHASING', u'MODELBUILDING'))
    method = Column(String(45))
    solventContent = Column(String(45))
    enantiomorph = Column(String(45))
    lowRes = Column(String(45))
    highRes = Column(String(45))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    AutoProcScaling = relationship(u'AutoProcScaling')
    PhasingProgramRun = relationship(u'PhasingProgramRun')
    SpaceGroup = relationship(u'SpaceGroup')


class PhasingHasScaling(Base):
    __tablename__ = 'Phasing_has_Scaling'

    phasingHasScalingId = Column(Integer, primary_key=True)
    phasingAnalysisId = Column(ForeignKey(u'PhasingAnalysis.phasingAnalysisId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    autoProcScalingId = Column(ForeignKey(u'AutoProcScaling.autoProcScalingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    datasetNumber = Column(Integer)
    recordTimeStamp = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    AutoProcScaling = relationship(u'AutoProcScaling')
    PhasingAnalysi = relationship('PhasingAnalysi')


class PlateGroup(Base):
    __tablename__ = 'PlateGroup'

    plateGroupId = Column(Integer, primary_key=True)
    name = Column(String(255))
    storageTemperature = Column(String(45))


class PlateType(Base):
    __tablename__ = 'PlateType'

    PlateTypeId = Column(Integer, primary_key=True)
    name = Column(String(45))
    description = Column(String(45))
    shape = Column(String(45))
    rowCount = Column(Integer)
    columnCount = Column(Integer)
    experimentId = Column(Integer, index=True)


class Position(Base):
    __tablename__ = 'Position'

    positionId = Column(Integer, primary_key=True)
    relativePositionId = Column(ForeignKey(u'Position.positionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    posX = Column(Float(asdecimal=True))
    posY = Column(Float(asdecimal=True))
    posZ = Column(Float(asdecimal=True))
    scale = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime)
    X = Column(Float(asdecimal=True))
    Y = Column(Float(asdecimal=True))
    Z = Column(Float(asdecimal=True))

    parent = relationship(u'Position', remote_side=[positionId])


class PreparePhasingDatum(Base):
    __tablename__ = 'PreparePhasingData'

    preparePhasingDataId = Column(Integer, primary_key=True)
    phasingAnalysisId = Column(ForeignKey(u'PhasingAnalysis.phasingAnalysisId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    phasingProgramRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    spaceGroupId = Column(ForeignKey(u'SpaceGroup.spaceGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime)

    PhasingAnalysi = relationship('PhasingAnalysi')
    PhasingProgramRun = relationship(u'PhasingProgramRun')
    SpaceGroup = relationship(u'SpaceGroup')


class ProcessingJob(Base):
    __tablename__ = 'ProcessingJob'

    processingJobId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    displayName = Column(String(80))
    comments = Column(String(255))
    recordTimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    recipe = Column(String(50))
    automatic = Column(Integer)

    DataCollection = relationship(u'DataCollection')


class ProcessingJobImageSweep(Base):
    __tablename__ = 'ProcessingJobImageSweep'

    processingJobImageSweepId = Column(Integer, primary_key=True)
    processingJobId = Column(ForeignKey(u'ProcessingJob.processingJobId'), index=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    startImage = Column(Integer)
    endImage = Column(Integer)

    DataCollection = relationship(u'DataCollection')
    ProcessingJob = relationship(u'ProcessingJob')


class ProcessingJobParameter(Base):
    __tablename__ = 'ProcessingJobParameter'

    processingJobParameterId = Column(Integer, primary_key=True)
    processingJobId = Column(ForeignKey(u'ProcessingJob.processingJobId'), index=True)
    parameterKey = Column(String(80))
    parameterValue = Column(String(255))

    ProcessingJob = relationship(u'ProcessingJob')


class Project(Base):
    __tablename__ = 'Project'

    projectId = Column(Integer, primary_key=True)
    personId = Column(ForeignKey(u'Person.personId'), index=True)
    title = Column(String(200))
    acronym = Column(String(100))
    owner = Column(String(50))

    Person = relationship(u'Person')
    XFEFluorescenceSpectrum = relationship(u'XFEFluorescenceSpectrum', secondary='Project_has_XFEFSpectrum')
    Protein = relationship(u'Protein', secondary='Project_has_Protein')
    Shipping = relationship(u'Shipping', secondary='Project_has_Shipping')
    BLSession = relationship(u'BLSession', secondary='Project_has_Session')


t_Project_has_BLSample = Table(
    'Project_has_BLSample', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('blSampleId', ForeignKey(u'BLSample.blSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_DCGroup = Table(
    'Project_has_DCGroup', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('dataCollectionGroupId', ForeignKey(u'DataCollectionGroup.dataCollectionGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_EnergyScan = Table(
    'Project_has_EnergyScan', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('energyScanId', ForeignKey(u'EnergyScan.energyScanId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_Person = Table(
    'Project_has_Person', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    Column('personId', ForeignKey(u'Person.personId', ondelete=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_Protein = Table(
    'Project_has_Protein', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    Column('proteinId', ForeignKey(u'Protein.proteinId', ondelete=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_Session = Table(
    'Project_has_Session', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('sessionId', ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_Project_has_Shipping = Table(
    'Project_has_Shipping', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    Column('shippingId', ForeignKey(u'Shipping.shippingId', ondelete=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


class ProjectHasUser(Base):
    __tablename__ = 'Project_has_User'

    projecthasuserid = Column(Integer, primary_key=True)
    projectid = Column(ForeignKey(u'Project.projectId'), nullable=False, index=True)
    username = Column(String(15))

    Project = relationship(u'Project')


t_Project_has_XFEFSpectrum = Table(
    'Project_has_XFEFSpectrum', Base.metadata,
    Column('projectId', ForeignKey(u'Project.projectId', ondelete=u'CASCADE'), primary_key=True, nullable=False),
    Column('xfeFluorescenceSpectrumId', ForeignKey(u'XFEFluorescenceSpectrum.xfeFluorescenceSpectrumId', ondelete=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


class Proposal(Base):
    __tablename__ = 'Proposal'
    __table_args__ = (
        Index('Proposal_FKIndexCodeNumber', 'proposalCode', 'proposalNumber', unique=True),
    )

    proposalId = Column(Integer, primary_key=True)
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    title = Column(String(200))
    proposalCode = Column(String(45))
    proposalNumber = Column(String(45))
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    proposalType = Column(String(2))
    externalId = Column(BINARY(16))

    Person = relationship(u'Person')


class ProposalHasPerson(Base):
    __tablename__ = 'ProposalHasPerson'

    proposalHasPersonId = Column(Integer, primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), nullable=False, index=True)
    personId = Column(ForeignKey(u'Person.personId'), nullable=False, index=True)
    role = Column(ENUM(u'Co-Investigator', u'Principal Investigator', u'Alternate Contact'))

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')


class Protein(Base):
    __tablename__ = 'Protein'
    __table_args__ = (
        Index('ProteinAcronym_Index', 'proposalId', 'acronym'),
    )

    proteinId = Column(Integer, primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    name = Column(String(255))
    acronym = Column(String(45), index=True)
    molecularMass = Column(Float(asdecimal=True))
    proteinType = Column(String(45))
    personId = Column(Integer, index=True)
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    isCreatedBySampleSheet = Column(Integer, server_default=text("'0'"))
    sequence = Column(Text)
    MOD_ID = Column(String(20))
    componentTypeId = Column(ForeignKey(u'ComponentType.componentTypeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    concentrationTypeId = Column(ForeignKey(u'ConcentrationType.concentrationTypeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    _global = Column('global', Integer, server_default=text("'0'"))
    externalId = Column(BINARY(16))
    density = Column(Float)
    abundance = Column(Float)

    ComponentType = relationship(u'ComponentType')
    ConcentrationType = relationship(u'ConcentrationType')
    Proposal = relationship(u'Proposal')
    ComponentSubType = relationship(u'ComponentSubType', secondary='Component_has_SubType')


class ProteinHasPDB(Base):
    __tablename__ = 'Protein_has_PDB'

    proteinhaspdbid = Column(Integer, primary_key=True)
    proteinid = Column(ForeignKey(u'Protein.proteinId'), nullable=False, index=True)
    pdbid = Column(ForeignKey(u'PDB.pdbId'), nullable=False, index=True)

    PDB = relationship(u'PDB')
    Protein = relationship(u'Protein')


class Reprocessing(Base):
    __tablename__ = 'Reprocessing'

    reprocessingId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    displayName = Column(String(80))
    comments = Column(String(255))
    recordTimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    recipe = Column(String(50))
    automatic = Column(Integer)

    DataCollection = relationship(u'DataCollection')


class ReprocessingImageSweep(Base):
    __tablename__ = 'ReprocessingImageSweep'

    reprocessingImageSweepId = Column(Integer, primary_key=True)
    reprocessingId = Column(ForeignKey(u'Reprocessing.reprocessingId'), index=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId'), index=True)
    startImage = Column(Integer)
    endImage = Column(Integer)

    DataCollection = relationship(u'DataCollection')
    Reprocessing = relationship(u'Reprocessing')


class ReprocessingParameter(Base):
    __tablename__ = 'ReprocessingParameter'

    reprocessingParameterId = Column(Integer, primary_key=True)
    reprocessingId = Column(ForeignKey(u'Reprocessing.reprocessingId'), index=True)
    parameterKey = Column(String(80))
    parameterValue = Column(String(255))

    Reprocessing = relationship(u'Reprocessing')


class RobotAction(Base):
    __tablename__ = 'RobotAction'

    robotActionId = Column(Integer, primary_key=True)
    blsessionId = Column(ForeignKey(u'BLSession.sessionId'), nullable=False, index=True)
    blsampleId = Column(ForeignKey(u'BLSample.blSampleId'), index=True)
    actionType = Column(ENUM(u'LOAD', u'UNLOAD', u'DISPOSE', u'STORE', u'WASH', u'ANNEAL'))
    startTimestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    endTimestamp = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    status = Column(ENUM(u'SUCCESS', u'ERROR', u'CRITICAL', u'WARNING', u'EPICSFAIL', u'COMMANDNOTSENT'))
    message = Column(String(255))
    containerLocation = Column(SmallInteger)
    dewarLocation = Column(SmallInteger)
    sampleBarcode = Column(String(45))
    xtalSnapshotBefore = Column(String(255))
    xtalSnapshotAfter = Column(String(255))

    BLSample = relationship(u'BLSample')
    BLSession = relationship(u'BLSession')


class Run(Base):
    __tablename__ = 'Run'

    runId = Column(Integer, primary_key=True)
    timePerFrame = Column(String(45))
    timeStart = Column(String(45))
    timeEnd = Column(String(45))
    storageTemperature = Column(String(45))
    exposureTemperature = Column(String(45))
    spectrophotometer = Column(String(45))
    energy = Column(String(45))
    creationDate = Column(DateTime)
    frameAverage = Column(String(45))
    frameCount = Column(String(45))
    transmission = Column(String(45))
    beamCenterX = Column(String(45))
    beamCenterY = Column(String(45))
    pixelSizeX = Column(String(45))
    pixelSizeY = Column(String(45))
    radiationRelative = Column(String(45))
    radiationAbsolute = Column(String(45))
    normalization = Column(String(45))


t_SAFETYREQUEST = Table(
    'SAFETYREQUEST', Base.metadata,
    Column('SAFETYREQUESTID', Numeric(10, 0)),
    Column('XMLDOCUMENTID', Numeric(10, 0)),
    Column('PROTEINID', Numeric(10, 0)),
    Column('PROJECTCODE', String(45)),
    Column('SUBMISSIONDATE', DateTime),
    Column('RESPONSE', Numeric(3, 0)),
    Column('REPONSEDATE', DateTime),
    Column('RESPONSEDETAILS', String(255))
)


class SAMPLECELL(Base):
    __tablename__ = 'SAMPLECELL'

    SAMPLECELLID = Column(Integer, primary_key=True)
    SAMPLEEXPOSUREUNITID = Column(Integer)
    ID = Column(String(45))
    NAME = Column(String(45))
    DIAMETER = Column(String(45))
    MATERIAL = Column(String(45))


class SAMPLEEXPOSUREUNIT(Base):
    __tablename__ = 'SAMPLEEXPOSUREUNIT'

    SAMPLEEXPOSUREUNITID = Column(Integer, primary_key=True)
    ID = Column(String(45))
    PATHLENGTH = Column(String(45))
    VOLUME = Column(String(45))


class SAXSDATACOLLECTIONGROUP(Base):
    __tablename__ = 'SAXSDATACOLLECTIONGROUP'

    DATACOLLECTIONGROUPID = Column(Integer, primary_key=True)
    DEFAULTDATAACQUISITIONID = Column(Integer)
    SAXSDATACOLLECTIONARRAYID = Column(Integer)


class SWOnceToken(Base):
    __tablename__ = 'SW_onceToken'

    onceTokenId = Column(Integer, primary_key=True)
    token = Column(String(128))
    personId = Column(ForeignKey(u'Person.personId'), index=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), index=True)
    validity = Column(String(200))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')


class SafetyLevel(Base):
    __tablename__ = 'SafetyLevel'

    safetyLevelId = Column(Integer, primary_key=True)
    code = Column(String(45))
    description = Column(String(45))


class SamplePlate(Base):
    __tablename__ = 'SamplePlate'

    samplePlateId = Column(Integer, primary_key=True)
    BLSESSIONID = Column(Integer)
    plateGroupId = Column(ForeignKey(u'PlateGroup.plateGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    plateTypeId = Column(ForeignKey(u'PlateType.PlateTypeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    instructionSetId = Column(ForeignKey(u'InstructionSet.instructionSetId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    boxId = Column(Integer)
    name = Column(String(45))
    slotPositionRow = Column(String(45))
    slotPositionColumn = Column(String(45))
    storageTemperature = Column(String(45))
    experimentId = Column(ForeignKey(u'Experiment.experimentId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    Experiment = relationship(u'Experiment')
    InstructionSet = relationship(u'InstructionSet')
    PlateGroup = relationship(u'PlateGroup')
    PlateType = relationship(u'PlateType')


class SamplePlatePosition(Base):
    __tablename__ = 'SamplePlatePosition'

    samplePlatePositionId = Column(Integer, primary_key=True)
    samplePlateId = Column(ForeignKey(u'SamplePlate.samplePlateId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    rowNumber = Column(Integer)
    columnNumber = Column(Integer)
    volume = Column(String(45))

    SamplePlate = relationship(u'SamplePlate')


class SaxsDataCollection(Base):
    __tablename__ = 'SaxsDataCollection'

    dataCollectionId = Column(Integer, primary_key=True)
    BLSESSIONID = Column(Integer)
    experimentId = Column(ForeignKey(u'Experiment.experimentId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    comments = Column(String(5120))

    Experiment = relationship(u'Experiment')


class ScanParametersModel(Base):
    __tablename__ = 'ScanParametersModel'

    scanParametersModelId = Column(Integer, primary_key=True)
    scanParametersServiceId = Column(ForeignKey(u'ScanParametersService.scanParametersServiceId', onupdate=u'CASCADE'), index=True)
    dataCollectionPlanId = Column(ForeignKey(u'DiffractionPlan.diffractionPlanId', onupdate=u'CASCADE'), index=True)
    sequenceNumber = Column(Integer)
    start = Column(Float(asdecimal=True))
    stop = Column(Float(asdecimal=True))
    step = Column(Float(asdecimal=True))
    array = Column(Text)
    duration = Column(Integer)

    DiffractionPlan = relationship(u'DiffractionPlan')
    ScanParametersService = relationship(u'ScanParametersService')


class ScanParametersService(Base):
    __tablename__ = 'ScanParametersService'

    scanParametersServiceId = Column(Integer, primary_key=True)
    name = Column(String(45))
    description = Column(String(45))


class Schedule(Base):
    __tablename__ = 'Schedule'

    scheduleId = Column(Integer, primary_key=True)
    name = Column(String(45))


class ScheduleComponent(Base):
    __tablename__ = 'ScheduleComponent'

    scheduleComponentId = Column(Integer, primary_key=True)
    scheduleId = Column(ForeignKey(u'Schedule.scheduleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    offset_hours = Column(Integer)
    inspectionTypeId = Column(ForeignKey(u'InspectionType.inspectionTypeId', ondelete=u'CASCADE'), index=True)

    InspectionType = relationship(u'InspectionType')
    Schedule = relationship(u'Schedule')


class SchemaStatu(Base):
    __tablename__ = 'SchemaStatus'

    schemaStatusId = Column(Integer, primary_key=True)
    scriptName = Column(String(100), nullable=False, unique=True)
    schemaStatus = Column(String(10))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class Screen(Base):
    __tablename__ = 'Screen'

    screenId = Column(Integer, primary_key=True)
    name = Column(String(45))
    proposalId = Column(ForeignKey(u'Proposal.proposalId'), index=True)
    _global = Column('global', Integer)

    Proposal = relationship(u'Proposal')


class ScreenComponent(Base):
    __tablename__ = 'ScreenComponent'

    screenComponentId = Column(Integer, primary_key=True)
    screenComponentGroupId = Column(ForeignKey(u'ScreenComponentGroup.screenComponentGroupId'), nullable=False, index=True)
    componentId = Column(ForeignKey(u'Protein.proteinId'), index=True)
    concentration = Column(Float)
    pH = Column(Float)

    Protein = relationship(u'Protein')
    ScreenComponentGroup = relationship(u'ScreenComponentGroup')


class ScreenComponentGroup(Base):
    __tablename__ = 'ScreenComponentGroup'

    screenComponentGroupId = Column(Integer, primary_key=True)
    screenId = Column(ForeignKey(u'Screen.screenId'), nullable=False, index=True)
    position = Column(SmallInteger)

    Screen = relationship(u'Screen')


class Screening(Base):
    __tablename__ = 'Screening'

    screeningId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    programVersion = Column(String(45))
    comments = Column(String(255))
    shortComments = Column(String(20))
    diffractionPlanId = Column(Integer, index=True)
    dataCollectionGroupId = Column(ForeignKey(u'DataCollectionGroup.dataCollectionGroupId'), index=True)
    xmlSampleInformation = Column(LONGBLOB)

    DataCollectionGroup = relationship(u'DataCollectionGroup')
    DataCollection = relationship(u'DataCollection')


class ScreeningInput(Base):
    __tablename__ = 'ScreeningInput'

    screeningInputId = Column(Integer, primary_key=True)
    screeningId = Column(ForeignKey(u'Screening.screeningId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    beamX = Column(Float)
    beamY = Column(Float)
    rmsErrorLimits = Column(Float)
    minimumFractionIndexed = Column(Float)
    maximumFractionRejected = Column(Float)
    minimumSignalToNoise = Column(Float)
    diffractionPlanId = Column(Integer)
    xmlSampleInformation = Column(LONGBLOB)

    Screening = relationship(u'Screening')


class ScreeningOutput(Base):
    __tablename__ = 'ScreeningOutput'

    screeningOutputId = Column(Integer, primary_key=True)
    screeningId = Column(ForeignKey(u'Screening.screeningId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    statusDescription = Column(String(1024))
    rejectedReflections = Column(Integer)
    resolutionObtained = Column(Float)
    spotDeviationR = Column(Float)
    spotDeviationTheta = Column(Float)
    beamShiftX = Column(Float)
    beamShiftY = Column(Float)
    numSpotsFound = Column(Integer)
    numSpotsUsed = Column(Integer)
    numSpotsRejected = Column(Integer)
    mosaicity = Column(Float)
    iOverSigma = Column(Float)
    diffractionRings = Column(Integer)
    SCREENINGSUCCESS = Column(Integer, server_default=text("'0'"))
    mosaicityEstimated = Column(Integer, nullable=False, server_default=text("'0'"))
    rankingResolution = Column(Float(asdecimal=True))
    program = Column(String(45))
    doseTotal = Column(Float(asdecimal=True))
    totalExposureTime = Column(Float(asdecimal=True))
    totalRotationRange = Column(Float(asdecimal=True))
    totalNumberOfImages = Column(Integer)
    rFriedel = Column(Float(asdecimal=True))
    indexingSuccess = Column(Integer, nullable=False, server_default=text("'0'"))
    strategySuccess = Column(Integer, nullable=False, server_default=text("'0'"))
    alignmentSuccess = Column(Integer, nullable=False, server_default=text("'0'"))

    Screening = relationship(u'Screening')


class ScreeningOutputLattice(Base):
    __tablename__ = 'ScreeningOutputLattice'

    screeningOutputLatticeId = Column(Integer, primary_key=True)
    screeningOutputId = Column(ForeignKey(u'ScreeningOutput.screeningOutputId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    spaceGroup = Column(String(45))
    pointGroup = Column(String(45))
    bravaisLattice = Column(String(45))
    rawOrientationMatrix_a_x = Column(Float)
    rawOrientationMatrix_a_y = Column(Float)
    rawOrientationMatrix_a_z = Column(Float)
    rawOrientationMatrix_b_x = Column(Float)
    rawOrientationMatrix_b_y = Column(Float)
    rawOrientationMatrix_b_z = Column(Float)
    rawOrientationMatrix_c_x = Column(Float)
    rawOrientationMatrix_c_y = Column(Float)
    rawOrientationMatrix_c_z = Column(Float)
    unitCell_a = Column(Float)
    unitCell_b = Column(Float)
    unitCell_c = Column(Float)
    unitCell_alpha = Column(Float)
    unitCell_beta = Column(Float)
    unitCell_gamma = Column(Float)
    bltimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    labelitIndexing = Column(Integer, server_default=text("'0'"))

    ScreeningOutput = relationship(u'ScreeningOutput')


class ScreeningRank(Base):
    __tablename__ = 'ScreeningRank'

    screeningRankId = Column(Integer, primary_key=True)
    screeningRankSetId = Column(ForeignKey(u'ScreeningRankSet.screeningRankSetId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    screeningId = Column(ForeignKey(u'Screening.screeningId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    rankValue = Column(Float)
    rankInformation = Column(String(1024))

    Screening = relationship(u'Screening')
    ScreeningRankSet = relationship(u'ScreeningRankSet')


class ScreeningRankSet(Base):
    __tablename__ = 'ScreeningRankSet'

    screeningRankSetId = Column(Integer, primary_key=True)
    rankEngine = Column(String(255))
    rankingProjectFileName = Column(String(255))
    rankingSummaryFileName = Column(String(255))


class ScreeningStrategy(Base):
    __tablename__ = 'ScreeningStrategy'

    screeningStrategyId = Column(Integer, primary_key=True)
    screeningOutputId = Column(ForeignKey(u'ScreeningOutput.screeningOutputId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    phiStart = Column(Float)
    phiEnd = Column(Float)
    rotation = Column(Float)
    exposureTime = Column(Float)
    resolution = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    anomalous = Column(Integer, nullable=False, server_default=text("'0'"))
    program = Column(String(45))
    rankingResolution = Column(Float)
    transmission = Column(Float)

    ScreeningOutput = relationship(u'ScreeningOutput')


class ScreeningStrategySubWedge(Base):
    __tablename__ = 'ScreeningStrategySubWedge'

    screeningStrategySubWedgeId = Column(Integer, primary_key=True)
    screeningStrategyWedgeId = Column(ForeignKey(u'ScreeningStrategyWedge.screeningStrategyWedgeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    subWedgeNumber = Column(Integer)
    rotationAxis = Column(String(45))
    axisStart = Column(Float)
    axisEnd = Column(Float)
    exposureTime = Column(Float)
    transmission = Column(Float)
    oscillationRange = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    RESOLUTION = Column(Float)
    doseTotal = Column(Float)
    numberOfImages = Column(Integer)
    comments = Column(String(255))

    ScreeningStrategyWedge = relationship(u'ScreeningStrategyWedge')


class ScreeningStrategyWedge(Base):
    __tablename__ = 'ScreeningStrategyWedge'

    screeningStrategyWedgeId = Column(Integer, primary_key=True)
    screeningStrategyId = Column(ForeignKey(u'ScreeningStrategy.screeningStrategyId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    wedgeNumber = Column(Integer)
    resolution = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    doseTotal = Column(Float)
    numberOfImages = Column(Integer)
    phi = Column(Float)
    kappa = Column(Float)
    chi = Column(Float)
    comments = Column(String(255))
    wavelength = Column(Float(asdecimal=True))

    ScreeningStrategy = relationship(u'ScreeningStrategy')


class SessionType(Base):
    __tablename__ = 'SessionType'

    sessionTypeId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    typeName = Column(String(31), nullable=False)

    BLSession = relationship(u'BLSession')


class SessionHasPerson(Base):
    __tablename__ = 'Session_has_Person'

    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    personId = Column(ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    role = Column(ENUM(u'Local Contact', u'Local Contact 2', u'Staff', u'Team Leader', u'Co-Investigator', u'Principal Investigator', u'Alternate Contact', u'Data Access', u'Team Member'))
    remote = Column(Integer, server_default=text("'0'"))

    Person = relationship(u'Person')
    BLSession = relationship(u'BLSession')


class Shipping(Base):
    __tablename__ = 'Shipping'

    shippingId = Column(Integer, primary_key=True)
    proposalId = Column(ForeignKey(u'Proposal.proposalId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    shippingName = Column(String(45), index=True)
    deliveryAgent_agentName = Column(String(45))
    deliveryAgent_shippingDate = Column(Date)
    deliveryAgent_deliveryDate = Column(Date)
    deliveryAgent_agentCode = Column(String(45))
    deliveryAgent_flightCode = Column(String(45))
    shippingStatus = Column(String(45), index=True)
    bltimeStamp = Column(DateTime)
    laboratoryId = Column(Integer, index=True)
    isStorageShipping = Column(Integer, server_default=text("'0'"))
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
    deliveryAgent_productcode = Column(String(10))
    deliveryAgent_flightCodePersonId = Column(ForeignKey(u'Person.personId'), index=True)

    Person = relationship(u'Person')
    Proposal = relationship(u'Proposal')
    LabContact = relationship(u'LabContact', primaryjoin='Shipping.returnLabContactId == LabContact.labContactId')
    LabContact1 = relationship(u'LabContact', primaryjoin='Shipping.sendingLabContactId == LabContact.labContactId')


t_ShippingHasSession = Table(
    'ShippingHasSession', Base.metadata,
    Column('shippingId', ForeignKey(u'Shipping.shippingId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True),
    Column('sessionId', ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


class SpaceGroup(Base):
    __tablename__ = 'SpaceGroup'

    spaceGroupId = Column(Integer, primary_key=True)
    spaceGroupNumber = Column(Integer)
    spaceGroupShortName = Column(String(45), index=True)
    spaceGroupName = Column(String(45))
    bravaisLattice = Column(String(45))
    bravaisLatticeName = Column(String(45))
    pointGroup = Column(String(45))
    geometryClassnameId = Column(ForeignKey(u'GeometryClassname.geometryClassnameId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    MX_used = Column(Integer, nullable=False, server_default=text("'0'"))

    GeometryClassname = relationship(u'GeometryClassname')


class Speciman(Base):
    __tablename__ = 'Specimen'

    specimenId = Column(Integer, primary_key=True)
    BLSESSIONID = Column(Integer)
    bufferId = Column(ForeignKey(u'Buffer.bufferId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    samplePlatePositionId = Column(ForeignKey(u'SamplePlatePosition.samplePlatePositionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    safetyLevelId = Column(ForeignKey(u'SafetyLevel.safetyLevelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    stockSolutionId = Column(ForeignKey(u'StockSolution.stockSolutionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    code = Column(String(255))
    concentration = Column(String(45))
    volume = Column(String(45))
    experimentId = Column(ForeignKey(u'Experiment.experimentId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    comments = Column(String(5120))

    Buffer = relationship(u'Buffer')
    Experiment = relationship(u'Experiment')
    Macromolecule = relationship(u'Macromolecule')
    SafetyLevel = relationship(u'SafetyLevel')
    SamplePlatePosition = relationship(u'SamplePlatePosition')
    StockSolution = relationship(u'StockSolution')


class StockSolution(Base):
    __tablename__ = 'StockSolution'

    stockSolutionId = Column(Integer, primary_key=True)
    BLSESSIONID = Column(Integer)
    bufferId = Column(ForeignKey(u'Buffer.bufferId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    instructionSetId = Column(ForeignKey(u'InstructionSet.instructionSetId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    boxId = Column(Integer)
    name = Column(String(45))
    storageTemperature = Column(String(55))
    volume = Column(String(55))
    concentration = Column(String(55))
    comments = Column(String(255))
    proposalId = Column(Integer, nullable=False, server_default=text("'-1'"))

    Buffer = relationship(u'Buffer')
    InstructionSet = relationship(u'InstructionSet')
    Macromolecule = relationship(u'Macromolecule')


class Stoichiometry(Base):
    __tablename__ = 'Stoichiometry'

    stoichiometryId = Column(Integer, primary_key=True)
    hostMacromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ratio = Column(String(45))

    Macromolecule = relationship(u'Macromolecule', primaryjoin='Stoichiometry.hostMacromoleculeId == Macromolecule.macromoleculeId')
    Macromolecule1 = relationship(u'Macromolecule', primaryjoin='Stoichiometry.macromoleculeId == Macromolecule.macromoleculeId')


class Structure(Base):
    __tablename__ = 'Structure'

    structureId = Column(Integer, primary_key=True)
    macromoleculeId = Column(ForeignKey(u'Macromolecule.macromoleculeId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    PDB = Column(String(45))
    structureType = Column(String(45))
    fromResiduesBases = Column(String(45))
    toResiduesBases = Column(String(45))
    sequence = Column(String(45))

    Macromolecule = relationship(u'Macromolecule')


class SubstructureDetermination(Base):
    __tablename__ = 'SubstructureDetermination'

    substructureDeterminationId = Column(Integer, primary_key=True)
    phasingAnalysisId = Column(ForeignKey(u'PhasingAnalysis.phasingAnalysisId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    phasingProgramRunId = Column(ForeignKey(u'PhasingProgramRun.phasingProgramRunId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    spaceGroupId = Column(ForeignKey(u'SpaceGroup.spaceGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    method = Column(ENUM(u'SAD', u'MAD', u'SIR', u'SIRAS', u'MR', u'MIR', u'MIRAS', u'RIP', u'RIPAS'))
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime)

    PhasingAnalysi = relationship('PhasingAnalysi')
    PhasingProgramRun = relationship(u'PhasingProgramRun')
    SpaceGroup = relationship(u'SpaceGroup')


class Subtraction(Base):
    __tablename__ = 'Subtraction'

    subtractionId = Column(Integer, primary_key=True)
    dataCollectionId = Column(ForeignKey(u'SaxsDataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    rg = Column(String(45))
    rgStdev = Column(String(45))
    I0 = Column(String(45))
    I0Stdev = Column(String(45))
    firstPointUsed = Column(String(45))
    lastPointUsed = Column(String(45))
    quality = Column(String(45))
    isagregated = Column(String(45))
    concentration = Column(String(45))
    gnomFilePath = Column(String(255))
    rgGuinier = Column(String(45))
    rgGnom = Column(String(45))
    dmax = Column(String(45))
    total = Column(String(45))
    volume = Column(String(45))
    creationTime = Column(DateTime)
    kratkyFilePath = Column(String(255))
    scatteringFilePath = Column(String(255))
    guinierFilePath = Column(String(255))
    SUBTRACTEDFILEPATH = Column(String(255))
    gnomFilePathOutput = Column(String(255))
    substractedFilePath = Column(String(255))

    SaxsDataCollection = relationship(u'SaxsDataCollection')


class SubtractionToAbInitioModel(Base):
    __tablename__ = 'SubtractionToAbInitioModel'

    subtractionToAbInitioModelId = Column(Integer, primary_key=True)
    abInitioId = Column(ForeignKey(u'AbInitioModel.abInitioModelId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    subtractionId = Column(ForeignKey(u'Subtraction.subtractionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)

    AbInitioModel = relationship(u'AbInitioModel')
    Subtraction = relationship(u'Subtraction')


class UserGroup(Base):
    __tablename__ = 'UserGroup'

    userGroupId = Column(Integer, primary_key=True)
    name = Column(String(31), nullable=False, unique=True)


t_UserGroup_has_Permission = Table(
    'UserGroup_has_Permission', Base.metadata,
    Column('userGroupId', ForeignKey(u'UserGroup.userGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('permissionId', ForeignKey(u'Permission.permissionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


t_UserGroup_has_Person = Table(
    'UserGroup_has_Person', Base.metadata,
    Column('userGroupId', ForeignKey(u'UserGroup.userGroupId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('personId', ForeignKey(u'Person.personId', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False, index=True)
)


class Workflow(Base):
    __tablename__ = 'Workflow'

    workflowId = Column(Integer, primary_key=True)
    workflowTitle = Column(String(255))
    workflowType = Column(ENUM(u'Undefined', u'BioSAXS Post Processing', u'EnhancedCharacterisation', u'LineScan', u'MeshScan', u'Dehydration', u'KappaReorientation', u'BurnStrategy', u'XrayCentering', u'DiffractionTomography', u'TroubleShooting', u'VisualReorientation', u'HelicalCharacterisation', u'GroupedProcessing', u'MXPressE', u'MXPressO', u'MXPressL', u'MXScore', u'MXPressI', u'MXPressM', u'MXPressA'))
    workflowTypeId = Column(Integer)
    comments = Column(String(1024))
    status = Column(String(255))
    resultFilePath = Column(String(255))
    logFilePath = Column(String(255))
    recordTimeStamp = Column(DateTime)
    workflowDescriptionFullPath = Column(String(255))


class WorkflowMesh(Base):
    __tablename__ = 'WorkflowMesh'

    workflowMeshId = Column(Integer, primary_key=True)
    workflowId = Column(ForeignKey(u'Workflow.workflowId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    bestPositionId = Column(ForeignKey(u'MotorPosition.motorPositionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    bestImageId = Column(ForeignKey(u'Image.imageId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    value1 = Column(Float(asdecimal=True))
    value2 = Column(Float(asdecimal=True))
    value3 = Column(Float(asdecimal=True))
    value4 = Column(Float(asdecimal=True))
    cartographyPath = Column(String(255))
    recordTimeStamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    Image = relationship(u'Image')
    MotorPosition = relationship(u'MotorPosition')
    Workflow = relationship(u'Workflow')


class WorkflowStep(Base):
    __tablename__ = 'WorkflowStep'

    workflowStepId = Column(Integer, primary_key=True)
    workflowId = Column(ForeignKey(u'Workflow.workflowId'), nullable=False, index=True)
    type = Column(String(45))
    status = Column(String(45))
    folderPath = Column(String(1024))
    imageResultFilePath = Column(String(1024))
    htmlResultFilePath = Column(String(1024))
    resultFilePath = Column(String(1024))
    comments = Column(String(2048))
    crystalSizeX = Column(String(45))
    crystalSizeY = Column(String(45))
    crystalSizeZ = Column(String(45))
    maxDozorScore = Column(String(45))
    recordTimeStamp = Column(DateTime)

    Workflow = relationship(u'Workflow')


class WorkflowType(Base):
    __tablename__ = 'WorkflowType'

    workflowTypeId = Column(Integer, primary_key=True)
    workflowTypeName = Column(String(45))
    comments = Column(String(2048))
    recordTimeStamp = Column(DateTime)


class XFEFluorescenceSpectrum(Base):
    __tablename__ = 'XFEFluorescenceSpectrum'

    xfeFluorescenceSpectrumId = Column(Integer, primary_key=True)
    sessionId = Column(ForeignKey(u'BLSession.sessionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    blSampleId = Column(ForeignKey(u'BLSample.blSampleId', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    jpegScanFileFullPath = Column(String(255))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    filename = Column(String(255))
    exposureTime = Column(Float)
    beamTransmission = Column(Float)
    annotatedPymcaXfeSpectrum = Column(String(255))
    fittedDataFileFullPath = Column(String(255))
    scanFileFullPath = Column(String(255))
    energy = Column(Float)
    beamSizeVertical = Column(Float)
    beamSizeHorizontal = Column(Float)
    crystalClass = Column(String(20))
    comments = Column(String(1024))
    blSubSampleId = Column(ForeignKey(u'BLSubSample.blSubSampleId'), index=True)
    flux = Column(Float(asdecimal=True))
    flux_end = Column(Float(asdecimal=True))
    workingDirectory = Column(String(512))

    BLSample = relationship(u'BLSample')
    BLSubSample = relationship(u'BLSubSample')
    BLSession = relationship(u'BLSession')


class XRFFluorescenceMapping(Base):
    __tablename__ = 'XRFFluorescenceMapping'

    xrfFluorescenceMappingId = Column(Integer, primary_key=True)
    xrfFluorescenceMappingROIId = Column(ForeignKey(u'XRFFluorescenceMappingROI.xrfFluorescenceMappingROIId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    dataCollectionId = Column(ForeignKey(u'DataCollection.dataCollectionId', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    imageNumber = Column(Integer, nullable=False)
    counts = Column(Integer, nullable=False)

    DataCollection = relationship(u'DataCollection')
    XRFFluorescenceMappingROI = relationship(u'XRFFluorescenceMappingROI')


class XRFFluorescenceMappingROI(Base):
    __tablename__ = 'XRFFluorescenceMappingROI'

    xrfFluorescenceMappingROIId = Column(Integer, primary_key=True)
    startEnergy = Column(Float, nullable=False)
    endEnergy = Column(Float, nullable=False)
    element = Column(String(2))
    edge = Column(String(2))
    r = Column(Integer)
    g = Column(Integer)
    b = Column(Integer)


t_v_Log4Stat = Table(
    'v_Log4Stat', Base.metadata,
    Column('id', Integer, server_default=text("'0'")),
    Column('priority', String(15)),
    Column('timestamp', DateTime),
    Column('msg', String(255)),
    Column('detail', String(255)),
    Column('value', String(255))
)


t_v_dewar = Table(
    'v_dewar', Base.metadata,
    Column('proposalId', Integer, server_default=text("'0'")),
    Column('shippingId', Integer, server_default=text("'0'")),
    Column('shippingName', String(45)),
    Column('dewarId', Integer, server_default=text("'0'")),
    Column('dewarName', String(45)),
    Column('dewarStatus', String(45)),
    Column('proposalCode', String(45)),
    Column('proposalNumber', String(45)),
    Column('creationDate', DateTime),
    Column('shippingType', String(45)),
    Column('barCode', String(45)),
    Column('shippingStatus', String(45)),
    Column('beamLineName', String(45)),
    Column('nbEvents', BigInteger, server_default=text("'0'")),
    Column('storesin', BigInteger, server_default=text("'0'")),
    Column('nbSamples', BigInteger, server_default=text("'0'"))
)


t_v_dewarBeamline = Table(
    'v_dewarBeamline', Base.metadata,
    Column('beamLineName', String(45)),
    Column('COUNT(*)', BigInteger, server_default=text("'0'"))
)


t_v_dewarBeamlineByWeek = Table(
    'v_dewarBeamlineByWeek', Base.metadata,
    Column('Week', String(2)),
    Column('ID14', BigInteger, server_default=text("'0'")),
    Column('ID23', BigInteger, server_default=text("'0'")),
    Column('ID29', BigInteger, server_default=text("'0'")),
    Column('BM14', BigInteger, server_default=text("'0'"))
)


t_v_dewarByWeek = Table(
    'v_dewarByWeek', Base.metadata,
    Column('Week', String(2)),
    Column('Dewars Tracked', BigInteger, server_default=text("'0'")),
    Column('Dewars Non-Tracked', BigInteger, server_default=text("'0'"))
)


t_v_dewarByWeekTotal = Table(
    'v_dewarByWeekTotal', Base.metadata,
    Column('Week', String(2)),
    Column('Dewars Tracked', BigInteger, server_default=text("'0'")),
    Column('Dewars Non-Tracked', BigInteger, server_default=text("'0'")),
    Column('Total', BigInteger, server_default=text("'0'"))
)


t_v_dewarList = Table(
    'v_dewarList', Base.metadata,
    Column('proposal', String(90)),
    Column('shippingName', String(45)),
    Column('dewarName', String(45)),
    Column('barCode', String(45)),
    Column('creationDate', String(10)),
    Column('shippingType', String(45)),
    Column('nbEvents', BigInteger, server_default=text("'0'")),
    Column('dewarStatus', String(45)),
    Column('shippingStatus', String(45)),
    Column('nbSamples', BigInteger, server_default=text("'0'"))
)


t_v_dewarProposalCode = Table(
    'v_dewarProposalCode', Base.metadata,
    Column('proposalCode', String(45)),
    Column('COUNT(*)', BigInteger, server_default=text("'0'"))
)


t_v_dewarProposalCodeByWeek = Table(
    'v_dewarProposalCodeByWeek', Base.metadata,
    Column('Week', String(2)),
    Column('MX', BigInteger, server_default=text("'0'")),
    Column('FX', BigInteger, server_default=text("'0'")),
    Column('BM14U', BigInteger, server_default=text("'0'")),
    Column('BM161', BigInteger, server_default=text("'0'")),
    Column('BM162', BigInteger, server_default=text("'0'")),
    Column('Others', BigInteger, server_default=text("'0'"))
)


t_v_hour = Table(
    'v_hour', Base.metadata,
    Column('num', String(18))
)


t_v_logonByHour = Table(
    'v_logonByHour', Base.metadata,
    Column('Hour', String(7)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByHour2 = Table(
    'v_logonByHour2', Base.metadata,
    Column('Hour', String(7)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByMonthDay = Table(
    'v_logonByMonthDay', Base.metadata,
    Column('Day', String(5)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByMonthDay2 = Table(
    'v_logonByMonthDay2', Base.metadata,
    Column('Day', String(5)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByWeek = Table(
    'v_logonByWeek', Base.metadata,
    Column('Week', String(2)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByWeek2 = Table(
    'v_logonByWeek2', Base.metadata,
    Column('Week', String(2)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByWeekDay = Table(
    'v_logonByWeekDay', Base.metadata,
    Column('Day', String(64)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_logonByWeekDay2 = Table(
    'v_logonByWeekDay2', Base.metadata,
    Column('Day', String(64)),
    Column('Distinct logins', BigInteger, server_default=text("'0'")),
    Column('Total logins', BigInteger, server_default=text("'0'"))
)


t_v_monthDay = Table(
    'v_monthDay', Base.metadata,
    Column('num', String(10))
)


t_v_run = Table(
    'v_run', Base.metadata,
    Column('runId', BigInteger, server_default=text("'0'")),
    Column('run', String(7)),
    Column('startDate', DateTime),
    Column('endDate', DateTime)
)


t_v_sample = Table(
    'v_sample', Base.metadata,
    Column('proposalId', Integer, server_default=text("'0'")),
    Column('shippingId', Integer, server_default=text("'0'")),
    Column('dewarId', Integer, server_default=text("'0'")),
    Column('containerId', Integer, server_default=text("'0'")),
    Column('blSampleId', Integer, server_default=text("'0'")),
    Column('proposalCode', String(45)),
    Column('proposalNumber', String(45)),
    Column('creationDate', DateTime),
    Column('shippingType', String(45)),
    Column('barCode', String(45)),
    Column('shippingStatus', String(45))
)


t_v_sampleByWeek = Table(
    'v_sampleByWeek', Base.metadata,
    Column('Week', String(2)),
    Column('Samples', BigInteger)
)


t_v_week = Table(
    'v_week', Base.metadata,
    Column('num', String(7))
)


t_v_weekDay = Table(
    'v_weekDay', Base.metadata,
    Column('day', String(10))
)
