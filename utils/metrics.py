import numpy as np

def RSE(pred, true):
    return np.sqrt(np.sum((true-pred)**2)) / np.sqrt(np.sum((true-true.mean())**2))

def CORR(pred, true):
    u = ((true-true.mean(0))*(pred-pred.mean(0))).sum(0) 
    d = np.sqrt(((true-true.mean(0))**2*(pred-pred.mean(0))**2).sum(0))
    return (u/d).mean(-1)

def MAE(pred, true):
    return np.mean(np.abs(pred-true))

def MSE(pred, true):
    return np.mean((pred-true)**2)

def RMSE(pred, true):
    return np.sqrt(MSE(pred, true))

def MAPE(pred, true):
    true = true.reshape(-1, 1)
    pred = pred.reshape(-1, 1)
    test_new = []
    predict_new = []
    for i in range(len(true)):
        if true[i,:] != 0:
            test_new.append(true[i,:])
            predict_new.append(pred[i,:])
    test_new = np.array(test_new)
    predict_new = np.array(predict_new)
    return np.mean(np.abs((predict_new - test_new) / test_new))


def MSPE(pred, true):
    true = true.reshape(-1, 1)
    pred = pred.reshape(-1, 1)
    test_new = []
    predict_new = []
    for i in range(len(true)):
        if true[i, :] != 0:
            test_new.append(true[i, :])
            predict_new.append(pred[i, :])
    test_new = np.array(test_new)
    predict_new = np.array(predict_new)
    return np.mean(np.square((predict_new - test_new) / test_new))

def metric(pred, true):
    mae = MAE(pred, true)
    mse = MSE(pred, true)
    rmse = RMSE(pred, true)
    mape = MAPE(pred, true)
    mspe = MSPE(pred, true)
    
    return mae,mse,rmse,mape,mspe