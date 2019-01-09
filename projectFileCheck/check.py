import os
import re
import json


def exit_terminal(error_message):
    os.system('rm projectFileCheck/project.pbxproj.json')
    raise NameError(error_message)

def load_config(key):
    try:
        with open('projectFileCheck/project_check.json', 'r') as f:
            configs = json.load(f)
            f.close()
            return configs[key]
    except:
        print("open config file '%s' failed" % 'project_check.json')
        exit_terminal("open config file error '%s'" % 'projectFileCheck/project_check.json')

def load_ignore_files():
    try:
        with open('projectFileCheck/ignore_files') as f:
            return list(map(lambda x: x.strip('\n'), f.readlines()))
    except:
        print("open config file '%s' failed" % 'ignore_files')
        exit_terminal("open config file error '%s'" % 'projectFileCheck/ignore_files')
    finally:
        f.close()

def run_command(command):
    result = os.system(command)
    if result > 0:
        exit_terminal("command error '%s'" % command)

def load_local_files(root_path, ignore_files):
    local_file_list = []
    for file in os.listdir(root_path):
        if len(list(filter(lambda x: re.match(x, file) != None, ignore_files))) != 0:
            continue
        full_path = os.path.join(root_path, file)
        if os.path.isdir(full_path):
            if load_local_files(full_path, ignore_files) != None:
                local_file_list = local_file_list + load_local_files(full_path, ignore_files)
        else:
            local_file_list.append(file)
    return local_file_list

def parse_project_file():
    run_command('plutil -convert json -s -r -o projectFileCheck/project.pbxproj.json %s/project.pbxproj' % load_config('project_file_path'))

def load_files_in_target(target_name):
    files_in_target = []
    try:
        with open('projectFileCheck/project.pbxproj.json', 'r') as f:
            project_file_json = json.load(f)
            root_key = project_file_json["rootObject"]
            objects = project_file_json["objects"]
            root_obj = objects[root_key]
            target_keys = root_obj["targets"]
            for target_key in target_keys:
                target = objects[target_key]
                if target['name'] == target_name:
                    buildPhase_keys = target['buildPhases']
                    for buildPhase_key in buildPhase_keys:
                        buildPhase = objects[buildPhase_key]
                        if buildPhase['isa'] == 'PBXSourcesBuildPhase':
                            file_keys = buildPhase["files"]
                            for file_key in file_keys:
                                try:
                                    file_ref = objects[file_key]
                                    file_ref_key = file_ref["fileRef"]
                                    file_name = objects[file_ref_key]
                                    files_in_target.append(file_name["path"])
                                except:
                                    continue
                        if buildPhase['isa'] == 'PBXResourcesBuildPhase':
                            file_keys = buildPhase["files"]
                            for file_key in file_keys:
                                try:
                                    file_ref = objects[file_key]
                                    file_ref_key = file_ref["fileRef"]
                                    file_name = objects[file_ref_key]
                                    files_in_target.append(file_name["path"])
                                except:
                                    continue
    
    except:
        exit_terminal("parse project json file error")
    return files_in_target

if __name__ == '__main__':
    error_files = {}
    parse_project_file()
    local_file_list = []
    for path in list(load_config('local_file_pathes')):
        local_file_list = local_file_list + load_local_files(path, list(load_ignore_files()))
    
    base_target = load_config('base_target')
    targets_need_to_check = list(load_config('targets_need_to_check'))

    base_target_files = load_files_in_target(base_target)
    for target in targets_need_to_check:
        target_files = load_files_in_target(target)
        for file in local_file_list:
            if file in target_files:
                continue
            
            if file in base_target_files:
                if target in error_files:
                    new_list =  error_files[target].append(file)
                else:
                    error_files[target] = [file]
    os.system('rm projectFileCheck/project.pbxproj.json')
    print(error_files)