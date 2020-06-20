from datetime import datetime
from Svalbard import db


class Additional_Metrics_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    Metrics = db.Column(db.String(1000), nullable=False)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fID = db.Column(db.String(100), unique=True, nullable=False)
    dataset_name = db.Column(db.String(50), unique=True, nullable=False)
    csv_link = db.Column(db.String(150), unique=True,
                         nullable=False, default='Web')
    size = db.Column(db.Integer, default=0)
    Meta = db.relationship('Metadata', backref='details', lazy=True)
    data = db.relationship('Result', backref='dataset', lazy=True)

    def __repr__(self):
        return f"Dataset('{self.id}', '{self.dataset_name}')"


class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Dataset_id = db.Column(db.Integer, db.ForeignKey(
        Dataset.id), nullable=False)
    NumericAttributes = db.Column(db.Integer, nullable=False)
    Instances = db.Column(db.Integer, nullable=False)
    Features = db.Column(db.Integer, nullable=False)
    Dimensionality = db.Column(db.Integer, nullable=False)
    PercentageOfMissingValues = db.Column(db.Integer, nullable=False)
    PercentageofInstancesWithMissingValues = db.Column(
        db.Float, nullable=False)
    PercentageBinaryFeatures = db.Column(db.Float, nullable=False)
    PercentageFeaturesWithMoreThan10Uniques = db.Column(
        db.Float, nullable=False)
    MaxCardinalityNumericFeatures = db.Column(db.Integer, nullable=False)
    MinCardinalityNumericFeatures = db.Column(db.Integer, nullable=False)
    MaxCardinalityNominalFeatures = db.Column(db.Integer, nullable=False)
    MinCardinalityNominalFeatures = db.Column(db.Integer, nullable=False)
    PercentageNumericFeatures = db.Column(db.Float, nullable=False)
    MinMean = db.Column(db.Float, nullable=False)
    MaxMean = db.Column(db.Float, nullable=False)
    MeanMean = db.Column(db.Float, nullable=False)
    MinStd = db.Column(db.Float, nullable=False)
    MaxStd = db.Column(db.Float, nullable=False)
    MeanStd = db.Column(db.Float, nullable=False)
    Q1Mean = db.Column(db.Float, nullable=False)
    Q2Mean = db.Column(db.Float, nullable=False)
    Q3Mean = db.Column(db.Float, nullable=False)
    Q1Std = db.Column(db.Float, nullable=False)
    Q2Std = db.Column(db.Float, nullable=False)
    Q3Std = db.Column(db.Float, nullable=False)
    NumberOfClasses = db.Column(db.Integer, nullable=False)
    MajorityClassPercentage = db.Column(db.Float, nullable=False)
    MinorityClassPercentage = db.Column(db.Float, nullable=False)
    MaximumCrossCorrelation = db.Column(db.Float)
    MinimumCrossCorrelation = db.Column(db.Float)
    MinSkew = db.Column(db.Float, nullable=False)
    MaxSkew = db.Column(db.Float, nullable=False)
    MeanSkew = db.Column(db.Float, nullable=False)
    Q1Skew = db.Column(db.Float, nullable=False)
    Q2Skew = db.Column(db.Float, nullable=False)
    Q3Skew = db.Column(db.Float, nullable=False)
    MinKutosis = db.Column(db.Float, nullable=False)
    MaxKutosis = db.Column(db.Float, nullable=False)
    MeanKutosis = db.Column(db.Float, nullable=False)
    Q1Kutosis = db.Column(db.Float, nullable=False)
    Q2Kutosis = db.Column(db.Float, nullable=False)
    Q3Kutosis = db.Column(db.Float, nullable=False)
    MaxMutualInformation = db.Column(db.Float, nullable=False)
    MinMutualInformation = db.Column(db.Float, nullable=False)
    Q1MutualInformation = db.Column(db.Float, nullable=False)
    Q2MutualInformation = db.Column(db.Float, nullable=False)
    Q3MutualInformation = db.Column(db.Float, nullable=False)
    MeanSignalToNoiseRatio = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Meta_of_Dataset('{self.Instances} \
            ', '{self.Features}', '{self.details}')"


class Metrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Accuracy = db.Column(db.Float, nullable=False)
    Precision = db.Column(db.Float, nullable=False)
    F1_Score = db.Column(db.Float, nullable=False)
    Recall = db.Column(db.Float, nullable=False)
    Time = db.Column(db.Float, nullable=False)
    Model = db.Column(db.String(100), nullable=False, default='Not Available')
    details = db.relationship('Result', backref='details', lazy=True)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey(
        'dataset.id'), nullable=False)
    task = db.Column(db.String(15), nullable=False)
    process = db.Column(db.String(20), nullable=False)
    platform = db.Column(db.String(15), nullable=False)
    metricsid = db.Column(db.Integer, db.ForeignKey(
        Metrics.id), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return f"Result('{self.task} \
            ', '{self.date_posted}', '{self.details.Accuracy}')"


class KNN_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='KNN_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    K = db.Column(db.Integer, nullable=False, default=5)
    weights = db.Column(db.String(50), nullable=False, default='uniform')
    algorithm = db.Column(db.String(50), nullable=False, default='auto')
    leaf_size = db.Column(db.Integer, nullable=False, default=30)
    distance_type = db.Column(
        db.String(50), nullable=False, default='Euclidean')
    n_jobs = db.Column(db.Integer, nullable=False, default=1)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))


class MLP_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='MLP_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    hidden_layer_neurons = db.Column(
        db.String, nullable=False, default='[100]')
    activation_fn = db.Column(db.String, nullable=False, default='relu')
    solver = db.Column(db.String, nullable=False, default='adam')
    alpha = db.Column(db.Float, nullable=False, default=0.0001)
    batch_size = db.Column(db.String, nullable=False, default='auto')
    learning_rate = db.Column(db.String, nullable=False, default='constant')
    learning_rate_value = db.Column(db.Float, nullable=False, default=0.001)
    max_iterations = db.Column(db.Integer, nullable=False, default=200)
    tolerance = db.Column(db.Float, nullable=False, default=0.0001)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))


class QDA_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='QDA_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))


class RF_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='RF_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    trees = db.Column(db.Integer, nullable=False, default=100)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))


class GNB_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='GNB_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))


class ABC_py(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resultid = db.Column(db.Integer, db.ForeignKey(
        'result.id'), nullable=False)
    result = db.relationship('Result', backref='ABC_result', lazy=True)
    eID = db.Column(db.String(100), nullable=False, unique=True)
    fID = db.Column(db.String(100), nullable=False)
    Additional = db.Column(db.Integer, db.ForeignKey(
        Additional_Metrics_py.id))

