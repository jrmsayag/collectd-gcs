# README #

A CollectD plugin to fetch Google Cloud Storage statistics.

## Install ##

```
pip install path-to-collectd-gcs.whl
```

or

```
python setup.py install
```

It is recommended to run the above commands in a [virtualenv](https://virtualenv.pypa.io/en/latest/) in order to prevent installed dependencies from interfering with system packages.

## Usage ##

Running command `collectdgcs bucket-name-where-logs-are-stored interval` periodically reads the logs written by Google Cloud Storage's Access & Storage Logs — which must therefore be enabled — in the given bucket, prints the results to the standard output in a format interpreted by [CollectD's Exec plugin](https://collectd.org/wiki/index.php/Plugin:Exec), and then removes the log files.

CollectD's configuration file must therefore contain the following lines that run the abovementionned command :

```
LoadPlugin exec

<Plugin exec>
  Exec user "collectdgcs" "logs-bucket-name" "interval"
</Plugin>
```

where `user` denotes a non-root user as specified in CollectD's Exec plugin documentation, and where the absolute path to `collectdgcs` should be specified instead if it was installed in a virtualenv.

You might want to create a dedicated user for collectd-gcs if no preexisting non-root user suits you, with :

```
sudo adduser --system --disabled-login --no-create-home collectdgcs
```

Also note that this plugin uses python package [google-cloud-storage](https://pypi.org/project/google-cloud-storage/) under the hood, so some configuration of Google Cloud Storage access authorizations might be needed for the above command to work properly. Refer to [google-cloud-storage's documentation](https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication) for details.

## Implementation notes ##

CollectD's Exec plugin is used instead of the [Python plugin](https://collectd.org/wiki/index.php/Plugin:Python), despite the latter being more features-rich, because the Python plugin is less convenient in terms of configuring the Python environment inside which collectd-gcs will be run. It is indeed a good idea to have collectd-gcs installed in a virtualenv in order not to break system-wide python packages since this plugin has some dependencies, and requires a specific Python version (>=3).
