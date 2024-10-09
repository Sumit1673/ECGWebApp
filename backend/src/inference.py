from PIL import Image
import io
import h5py
import numpy as np
from tensorflow.keras.models import load_model
from ml4h.models.model_factory import get_custom_objects
from ml4h.tensormap.ukb.survival import mgb_afib_wrt_instance2
from ml4h.tensormap.ukb.demographics import age_2_wide, af_dummy, sex_dummy3
from config import ENV, config, ecg_rest_leads, ecg_shape


def hd5_to_tensor(contents):
    with h5py.File(io.BytesIO(contents), 'r') as hd5:
        try:
            tensor = np.zeros(ecg_shape, dtype=np.float32)
            for lead in ecg_rest_leads:
                data = np.array(hd5[f'{config.get(ENV, "ECG_HD5_PATH")}/{lead}/instance_0'])
                tensor[:, ecg_rest_leads[lead]] = data
            tensor -= np.mean(tensor)
            tensor /= np.std(tensor) + 1e-6
    
            print(f"Tensor shape: {tensor.shape}")
            return tensor

        except Exception as e:
            print(f"Error: {e}")


def predict(file_contents):
    tensor = hd5_to_tensor(file_contents)
    try:
        tensor = np.expand_dims(tensor, axis=0)
        output_tensormaps = {tm.output_name(): tm for tm in [mgb_afib_wrt_instance2,
                                                            age_2_wide, af_dummy,
                                                            sex_dummy3]}
        custom_dict = get_custom_objects([mgb_afib_wrt_instance2, age_2_wide,
                                        af_dummy, sex_dummy3])
        
        model = load_model(config.get(ENV, 'MODEL_NAME'), custom_objects=custom_dict)
        
        prediction = model(tensor)
    except ValueError as e:
        print(e)
        return -1
    
    prediction_text = []
    for name, pred in zip(model.output_names, prediction):
        otm = output_tensormaps[name]
        if otm.is_survival_curve():
            intervals = otm.shape[-1] // 2
            predicted_survivals = np.cumprod(pred[:, :intervals], axis=1)
            print(f'AF Risk Survival Curve prediction is: {str(1 - predicted_survivals[0, -1])}')
            prediction_text.append(f'AF Risk Survival Curve prediction is: {str(1 - predicted_survivals[0, -1])}')
        else:
            print(f'{otm.name} prediction is {pred}')
            prediction_text.append(f'{otm.name} prediction is {pred}')
    return " ".join(prediction_text)

