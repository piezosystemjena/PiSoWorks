Waveform Generator
===================

The NV200 device has an arbitrary waveform generator. This waveform generator can be used
to generate a variety of waveforms. The arbitrary waveform generator can generate a single or 
repetitive setpoint signal. The curve shape can be freely defined by up to 1024 samples.

.. image:: images/waveform_numbered.png

The waveform generator can be used in either open-loop or closed-loop mode. Before creating a waveform, 
please select the appropriate mode in the Easy Mode section or in the Settings panel. Depending on the 
selected mode, the waveform values must be entered in the software either as voltage values (V) or as 
position values.

You can show the Waveform panel by clicking the :guilabel:`Waveform` tab :guinum:`❶`. The Waveform UI 
has the following components:

:guinum:`❷` Waveform Settings
    Allows you to select the waveform type and configure its parameters. Changed parameters are highlighted
    in orange. This indicates that you need to reupload the waveform to the generator.

:guinum:`❸` Data Recorder
    Configure which data should be recorded during waveform playback.

:guinum:`❹` Generator Control
    Configure the number of cycles the generator should repeat the waveform and start or stop the generator.

:guinum:`❺` Data Recorder Plot
    Provides a visual representation of the generated waveform (light blue) that is updated as soon as the 
    waveform parameters are changed. It also shows the recorded data (green, orange) recorded during 
    waveform playback.


Generating a Waveform
---------------------------

With the software, you can generate predefined mathematical waveforms (sine, triangle, square) or 
load arbitrary waveforms from an Excel or CSV file. On the left side, in the :guilabel:`Waveform Settings`
panel, you can select the desired waveform type and configure its parameters.


Generating a Standard Waveform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To generate a standard waveform, follow these steps:

.. image:: images/waveform_settings.png

.. rst-class:: guinums

1. In the :guilabel:`Waveform` combobox :guinum:`❷`, select the desired waveform type (e.g., sine, triangle, square).
2. Configure the waveform frequency as needed. The waveform preview (light blue) and the :guilabel:`Sampling Period` will be updated accordingly.
3. Select the desired phase shift in the :guilabel:`Phase Shift` field.
4. Configure the waveform amplitude using the :guilabel:`High Level` and :guilabel:`Low Level` fields.
5. Finally, click the :guilabel:`Upload` button to send the waveform to the device.


Loading an Arbitrary Waveform
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to load an arbitrary waveform, the steps are slightly different from generating a standard waveform:

.. image:: images/waveform_arbitrary.png

.. rst-class:: guinums

1. In the :guilabel:`Waveform` combobox :guinum:`❷`, select the waveform type *Custom*.
2. Configure the :guilabel:`Sampling Period` - this determines how fast the sample values are processed in the device.
3. Click the :guilabel:`Load CSV / Excel` button to open a file dialog and then select the desired file. The waveform preview should show the loaded waveform (light blue).
4. Click the :guilabel:`Upload` button to send the waveform data to the device.


Running a Waveform
---------------------------

In the **Generator Control** section, you can control the waveform playback:

.. image:: images/waveform_generator_control.png

.. rst-class:: guinums

1. Configure the number of cycles in the :guilabel:`Cycles` field. This determines how many times the waveform will be repeated.
2. The total duration is updated automatically based on the number of cycles and the waveform frequency.
3. If you activate the :guilabel:`Sync Rec. Duration` switch, the recording duration will be synchronized automatically with the waveform duration.
4. Click the :guilabel:`Start` button to begin waveform playback and the :guilabel:`Stop` button to stop it.


Setting Up Data Recording   
---------------------------

In the **Data Recorder** section, you can configure which data should be recorded during waveform playback:

.. image:: images/data_recorder_settings.png

.. rst-class:: guinums

1. Use the :guilabel:`Channel` comboboxes to select the desired recording sources for both channels.
2. Configure the recording duration. If the :guilabel:`Sync Rec. Duration` switch is activated in the **Generator Control** section, 
   the recording duration will be synchronized automatically with the waveform duration.
3. The sampling period is updated accordingly. Longer recording durations lead to a lower sampling rate because the internal device data recorder is limited to 6144 data points.


