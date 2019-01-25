# Xcode-project-file-check

it's used for check the project file
if the project have more than one targets, when add source files may miss to check some target, use this script can check if all you need is contain in the project file.


## project_check.json

all the file path blow means the relative path to the project root path

|key|value type | required |meaning|
| :--- | :--- | :--- | :--- |
| project_file_path | String | true | the .xcodeproj file path |
| base_target | String | false | all the target need to check based on which target |
| targets_need_to_check | Array | true | all the target need to check
| local_file_pathes | Array | true | all the local filder in the project need to check |

## ignore_files

add all files and filders which is not need to check, you can use Regular Expressions also
one file or one Regular Expression in one line
when use Regular Expressions please make sure the reg is worked in python

## useage

after config all above, you can copy the projectFileCheck filder to the project root path, and add the script blow in the Build Phases

```sh

python scripts/projectFileCheck/check.py

if [ $? -ne 0 ]; then
    exit 1
fi
```


## on the way

1. add specific ignore files for different target to seprate the check for different target
