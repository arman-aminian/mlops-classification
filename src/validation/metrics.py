from sklearn.metrics import precision_score, recall_score, average_precision_score, roc_auc_score


def get_metrics(y_true, y_pred, threshold):
    predicted_label = list(map(lambda x: 1 if (x > threshold) else 0, y_pred))
    precision = precision_score(y_true, predicted_label)
    recall = recall_score(y_true, predicted_label)
    average_precision = average_precision_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_pred)

    return precision, recall, average_precision, roc_auc
