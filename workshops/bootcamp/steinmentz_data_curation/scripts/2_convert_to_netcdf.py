from functools import lru_cache
from pathlib import Path
from typing import Any
import numpy as np
from tqdm import tqdm
from xarray import DataArray, Dataset, Coordinates


@lru_cache
def get_brain_group_dict() -> dict[str, str]:
    brain_groups = {}
    for area in ["VISa", "VISam", "VISl", "VISp", "VISpm", "VISrl"]:
        brain_groups[area] = 'visual cortex'
    for area in ["CL", "LD", "LGd", "LH", "LP", "MD", "MG", "PO", "POL", "PT", "RT", "SPF", "TH", "VAL", "VPL", "VPM"]:
        brain_groups[area] = 'thalamus'
    for area in ["CA", "CA1", "CA2", "CA3", "DG", "SUB", "POST"]:
        brain_groups[area] = 'hippocampus'
    for area in ["ACA", "AUD", "COA", "DP", "ILA", "MOp", "MOs", "OLF", "ORB", "ORBm", "PIR", "PL", "SSp", "SSs", "RSP"," TT"]:
        brain_groups[area] = 'non-visual cortex'
    for area in ["APN", "IC", "MB", "MRN", "NB", "PAG", "RN", "SCs", "SCm", "SCig", "SCsg", "ZI"]:
        brain_groups[area] = 'midbrain'
    for area in ["ACB", "CP", "GPe", "LS", "LSc", "LSr", "MS", "OT", "SNr", "SI"]:
        brain_groups[area] = 'basal ganglia'
    for area in ["BLA", "BMA", "EP", "EPd", "MEA"]:
        brain_groups[area] = 'cortical subplate'
    return brain_groups



def steinmetz_to_xarray(dd: dict[str, Any]) -> Dataset:
    assert list(dd['ccf_axes']) == ['ap', 'dv', 'lr']
    dset = Dataset(
        dict(
            # Stimulus Data
            contrast_left = DataArray(
                data=(np.concatenate(
                    (dd['contrast_left'], dd['contrast_left_passive']),
                ) * 100).astype(np.int8),
                dims=('trial',)
            ),
            contrast_right = DataArray(
                data=(np.concatenate(
                    (dd['contrast_right'], dd['contrast_right_passive']),
                ) * 100).astype(np.int8),
                dims=('trial',)
            ),
            gocue = DataArray(
                data=np.concatenate((dd['gocue'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            stim_onset = DataArray(
                data=np.repeat([dd['stim_onset']], repeats=dd['active_trials'].shape[0]),
                dims=('trial'),
            ),
            feedback_type = DataArray(
                data=np.concatenate((dd['feedback_type'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            feedback_time = DataArray(
                data=np.concatenate((dd['feedback_time'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            response_type = DataArray(
                data=np.concatenate((dd['response'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            response_time = DataArray(
                data=np.concatenate((dd['response_time'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            reaction_type = DataArray(
                data=np.concatenate((dd['reaction_time'][:, 1], [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            reaction_time = DataArray(
                data=np.concatenate((dd['reaction_time'][:, 0], [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            prev_reward = DataArray(
                data=np.concatenate((dd['prev_reward'].squeeze(), [np.nan] * dd['licks_passive'].shape[1])), 
                dims=('trial',),
            ),
            active_trials = DataArray(data=dd['active_trials'], dims=('trial',)),

            # Wheel data
            wheel = DataArray(
                data=np.concatenate(
                    (dd['wheel'].squeeze(), dd['wheel_passive'].squeeze()), 
                    axis=0,
                ).astype(np.int8),
                dims=('trial', 'time')
            ),

            # Licks data
            licks = DataArray(
                data=np.concatenate(
                    (dd['licks'].squeeze(), dd['licks_passive'].squeeze()),
                    axis=0,
                ).astype(np.int8),
                dims=('trial', 'time'),
            ),

            # Pupil data
            pupil_x = DataArray(
                data=np.concatenate(
                    (dd['pupil'][1, :, :], dd['pupil_passive'][1, :, :]),
                    axis=0,
                ),
                dims=('trial', 'time')
            ),
            pupil_y = DataArray(
                data=np.concatenate(
                    (dd['pupil'][2, :, :], dd['pupil_passive'][2, :, :]),
                    axis=0,
                ),
                dims=('trial', 'time')
            ),
            pupil_area = DataArray(
                data=np.concatenate(
                    (dd['pupil'][0, :, :], dd['pupil_passive'][0, :, :]),
                    axis=0,
                ),
                dims=('trial', 'time')
            ),

            # Face data
            face = DataArray(
                data=np.concatenate(
                    (dd['face'].squeeze(), dd['face_passive'].squeeze()),
                    axis=0,
                ),
                dims=('trial', 'time'),
            ),

            # Spike data
            spks = DataArray(
                data=np.concatenate(
                    (dd['spks'], dd['spks_passive']),
                    axis=1,
                ).astype(np.int8), 
                dims=('cell', 'trial', 'time')
            ),
            trough_to_peak = DataArray(data=dd['trough_to_peak'].astype(np.int8), dims=('cell',)),
            ccf_ap = DataArray(data=dd['ccf'][:, 0], dims=('cell',)),
            ccf_dv = DataArray(data=dd['ccf'][:, 1], dims=('cell',)),
            ccf_lr = DataArray(data=dd['ccf'][:, 2], dims=('cell',)),
            brain_area = DataArray(data=dd['brain_area'], dims=('cell',)),
            
            brain_groups = DataArray(
                data=[get_brain_group_dict().get(area, area) for area in dd['brain_area']],
                dims=('cell',)
            ),
            
        ),
        coords=Coordinates({
            'trial': np.arange(1, dd['active_trials'].shape[0] + 1),
            'time': (np.arange(1, dd['wheel'].shape[-1] + 1) * dd['bin_size']),
            'cell': np.arange(1, dd['spks'].shape[0] + 1),
        }),
        attrs={
            'bin_size': dd['bin_size'],
            'stim_onset': dd['stim_onset'],
        }
    ).expand_dims({
        'mouse': [dd['mouse_name']],
        'session_date': [dd['date_exp']],
    })
    return dset



if __name__ == '__main__':

    base_path = Path('data/processed/neuropixels')
    base_path.mkdir(parents=True, exist_ok=True)

    for path in tqdm(list(Path('data/raw/neuropixels').glob('*.npz')), desc="Reading Raw NPZ Files"):
        dat = np.load(path, allow_pickle=True)['dat']

        for dd in tqdm(dat, desc=f"Writing Processed NetCDF Files from {path.name}"):
            dset = steinmetz_to_xarray(dd=dd)

            # Compression settings for each variable. 
            # Slower to write, but shrunk data to 6% the original size!
            settings = {'zlib': True, 'complevel': 5}
            encodings = {var: settings for var in dset.data_vars if not 'U' in str(dset[var].dtype)}
            
            dset.to_netcdf(
                path=base_path / f'steinmetz_{dd["date_exp"]}_{dd["mouse_name"]}.nc',
                format="NETCDF4",
                engine="netcdf4",
                encoding=encodings,   
            )
