import subprocess
import argparse


def down_url(model, n_member, experiment):
    head = "http://iridl.ldeo.columbia.edu/SOURCES/.Models/.NMME/."
    
    if experiment == 'monthly':
        exp = "/.MONTHLY"
    elif experiment == 'HINDCAST_monthly':
        exp = "/.HINDCAST/.MONTHLY"
    elif experiment == 'FORECAST_monthly':
        exp = "/.FORECAST/.MONTHLY"
    
    url = head + model + exp + f"/.sst/M/\({n_member}.0\)/\({n_member}.0\)/RANGEEDGES/data.nc"

    return url
    
    
def downloader(url, path, model, n_member, experiment):

    if experiment == 'FORECAST_monthly':
        settings = f" -P {path} -O {model}_F_{n_member}.nc"
    else:
        settings = f" -P {path} -O {model}_{n_member}.nc"

    cmd = "wget " + url + settings
    
    subprocess.run(cmd, shell = True)
    
    
    
if __name__ == '__main__':
    
    path = '/disk1/tywang/data/NMME/original/'
    num_member = range(1, 11)
    model = 'CMC1-CanCM3'
    experiment = 'FORECAST_monthly'
    
    for i in num_member:
        url = down_url(model, i, experiment)
        downloader(url, path, model, i, experiment)