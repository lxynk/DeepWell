import numpy as np


def predict_with_disagreement(model, X):
    """
    Predict success probabilities and tree disagreement for a fitted Random Forest.
    Disagreement is the standard deviation of individual trees' success probabilities.
    """
    tree_probs = np.array([
        tree.predict_proba(X)[:, list(tree.classes_).index(1)]
        for tree in model.estimators_
    ])

    mean_prob = tree_probs.mean(axis=0)
    disagreement = tree_probs.std(axis=0)

    return mean_prob, disagreement