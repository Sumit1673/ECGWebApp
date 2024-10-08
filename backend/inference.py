from PIL import Image

import h5py
import numpy as np
from tensorflow.keras.models import load_model
from ml4h.models.model_factory import get_custom_objects
from ml4h.tensormap.ukb.survival import mgb_afib_wrt_instance2
from ml4h.tensormap.ukb.demographics import age_2_wide, af_dummy, sex_dummy3
from config import ENV, config


def pre_process_hd5(ecg_file):
     with h5py.File(ecg_file, 'r') as hd5:
        tensor = np.zeros(config.get(ENV, "ECG_SHAPE"), dtype=np.float32)
        for lead in config.get(ENV, "ECG_REST_LEADS"):
            data = np.array(hd5[f'{config.get(ENV, 'ECG_HD5_PATH')}/{lead}/instance_0'])
            tensor[:, config.get(ENV, "ECG_REST_LEADS")[lead]] = data
        tensor -= np.mean(tensor)
        tensor /= np.std(tensor) + 1e-6
        # print(tensor.shape)
        return tensor
     
def predict(fullimgpath="data/fake_0.hd5"):
    tensor = pre_process_hd5('ecg/fake_0.hd5')
    tensor = np.expand_dims(tensor, axis=0)
    output_tensormaps = {tm.output_name(): tm for tm in [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]}
    custom_dict = get_custom_objects([mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3])
    model = load_model('ecg_5000_survival_curve_af_quadruple_task_mgh_v2021_05_21.h5',
                    custom_objects=custom_dict)
    prediction = model(tensor)
    for name, pred in zip(model.output_names, prediction):
        otm = output_tensormaps[name]
        print(otm)
        if otm.is_survival_curve():
            intervals = otm.shape[-1] // 2
            days_per_bin = 1 + otm.days_window // intervals
            predicted_survivals = np.cumprod(pred[:, :intervals], axis=1)
            print(type(otm))
            print(f'AF Risk {str(otm)} prediction is: {str(1 - predicted_survivals[0, -1])}')
        else:
            print(f'{otm} prediction is {pred}')
    return prediction


