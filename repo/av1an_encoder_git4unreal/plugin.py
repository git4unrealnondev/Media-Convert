from unmanic.libs.unplugins.settings import PluginSettings
from unmanic.libs.system import System

class Settings(PluginSettings):
    """
    An object to hold a dictionary of settings accessible to the Plugin
    class and able to be configured by users from within the Unmanic WebUI.

    This class has a number of methods available to it for accessing these settings:

        > get_setting(<key>)            - Fetch a single setting value. Or leave the
                                        key argument empty and return the full dictionary.
        > set_setting(<key>, <value>)   - Set a singe setting value.
                                        Used by the Unmanic WebUI to save user settings.
                                        Settings are stored on disk in order to be persistent.

    """
    settings = {
        "check_length": True,
        "Insert string into cache file name": "custom-string"
    }
    form_settings = {
        "check_length": {
            "label": "Would you like to check if the length of a file is longer than 265?",
        }


def on_worker_process(data):
    """
    Runner function - enables additional configured processing jobs during the worker stages of a task.

    The 'data' object argument includes:
        worker_log              - Array, the log lines that are being tailed by the frontend. Can be left empty.
        library_id              - Number, the library that the current task is associated with.
        exec_command            - Array, a subprocess command that Unmanic should execute. Can be empty.
        command_progress_parser - Function, a function that Unmanic can use to parse the STDOUT of the command to collect progress stats. Can be empty.
        file_in                 - String, the source file to be processed by the command.
        file_out                - String, the destination that the command should output (may be the same as the file_in if necessary).
        original_file_path      - String, the absolute path to the original file.
        repeat                  - Boolean, should this runner be executed again once completed with the same variables.

    :param data:
    :return:
    """
    settings = Settings(library_id=data.get('library_id'))
    system = System()
    system_info = system.info()

    custom_string = settings.get_setting('Insert string into cache file name')
    if custom_string:
        tmp_file_out = os.path.splitext(data['file_out'])
        data['file_out'] = "{}-{}-{}{}".format(tmp_file_out[0], custom_string, tmp_file_out[1])

    if not settings.get_setting('Execute Command'):
        data['exec_command'] = "av1an -i " + data["file_in"] + " -o " data["file_out"]



    return data