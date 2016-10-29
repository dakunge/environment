import json, sys, datetime, math, os, commands
from collections import defaultdict
# input
etcd_file = 'data/etcd_conf.json'
pbr_file = ''
id_file = ''
# output
module_file=''
user_file = ''
# debug
debug=''
# inter user
inter_user = {}

pbrecord_max_talent = {}
pbmodule_max_talent = {}
pb_metaid_count = {}
pb_moduleid_count = {}
pb_oneday_metaid_total = {}
pb_oneday_moduleid_total = {}
user_property = {}
day_flag=0 
config={}
offset = 0
maxidcount = 0

def getfile():
    global pbr_file, id_file, module_file, user_file
    time = datetime.datetime.now().strftime('%Y%m%d%H')
    pbr_file = 'data/pbplayrecords_' + time + '.json'
    id_file = 'data/id_counter_' + time + '.json'
    userfile = 'data/userproperties_' + time + '.json'

    module_file = 'result/module_' + time + '.json'
    user_file = 'result/user_' + time + '.json'

    pbplayrecord = '/home/muababa/mongodb-linux-x86_64-ubuntu1404-3.2.0/bin/mongoexport --host=10.251.211.45 --port=37017 --db uc --collection pbplayrecords --out ' + pbr_file
    idcounter = '/home/muababa/mongodb-linux-x86_64-ubuntu1404-3.2.0/bin/mongoexport --host=10.251.211.45 --port=37017 --db uc --collection id_counter --out ' + id_file
    userproperties = '/home/muababa/mongodb-linux-x86_64-ubuntu1404-3.2.0/bin/mongoexport --host=10.251.211.45 --port=37017 --db uc --collection userproperties --out ' + userfile
    
    if os.path.exists(pbr_file) or os.path.exists(id_file) or os.path.exists(userfile) or os.path.exists(module_file) or os.path.exists(user_file):
        sys.exit('file exists')
    
    a, b = commands.getstatusoutput(pbplayrecord)
    if a != 0:
        sys.exit(pbplayrecord+'\n' + b)
    
    a, b = commands.getstatusoutput(idcounter)
    if a != 0:
        sys.exit(idcounter+'\n' + b)
    
    a, b = commands.getstatusoutput(userproperties)
    if a != 0:
        sys.exit(idcounter+'\n' + b)

def musicradio(data, config):
    if config.get('is_offline', False) == False:
        musicradioonline(config, data)
    else:
        musicradiooffline(config, data)

def musicradioonline(config, data):
    if 'is_push' in data['meta']:
        pass
    else:
        return
    ifpush = data['meta']['is_push']
    if ifpush:
        c = config['push']
    else:
        c = config['not_push']

    exp = c['exp']['value']*data['value']
    talent = c['talent']['value']*data['value']
    bean = c['mua_bean']['value']*data['value']

# TODO one day?
    count = get_and_update_one_day_times(data)
    if count > 0:
        d = math.pow(config['exp_times_decrease']['percentage_decrease'], count)
        exp = exp * d
        bean = bean * d
        if exp < config['exp_times_decrease']['min_value']:
            exp = config['exp_times_decrease']['min_value']
        if bean < config['exp_times_decrease']['min_value']:
            bean = config['exp_times_decrease']['min_value']

    texp, tbean = get_and_update_one_day_total_exp_and_bean_by_module_id(data, exp, bean)
    if texp > c['exp']['max_value']:
        exp = c['exp']['exceed_value']
    if tbean > c['mua_bean']['max_value']:
        bean = c['mua_bean']['exceed_value']
    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'], talent-maxtalent,c['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, c['talent']['component_ratio'])

def musicradiooffline(config, data):
    c = config['push']
    exp = c['exp']['value']*data['value']
    talent = c['talent']['value']*data['value']
    bean = c['mua_bean']['value']*data['value']

    count = get_and_update_one_day_times(data)
    if count > 0:
        d = math.pow(config['exp_times_decrease']['percentage_decrease'], count)
        exp = exp * d
        bean = bean * d
        if exp < config['exp_times_decrease']['min_value']:
            exp = config['exp_times_decrease']['min_value']
        if bean < config['exp_times_decrease']['min_value']:
            bean = config['exp_times_decrease']['min_value']

    texp, tbean = get_and_update_one_day_total_exp_and_bean_by_module_id(data, exp, bean)
    if texp > c['exp']['max_value']:
        exp = c['exp']['exceed_value']
    if tbean > c['mua_bean']['max_value']:
        bean = c['mua_bean']['exceed_value']
    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'], talent-maxtalent,c['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, c['talent']['component_ratio'])

def playsound(data, config):
    if config.get('is_offline', False) == False:
        playsoundonline(config, data)
    else:
        playsoundoffline(config, data)

def playsoundonline(config, data):
    exp, bean, talent = get_value(config, data)
    if 'id' in data['meta']:
        pass
    else:
        return
    count = get_and_update_one_day_times(data)
    if count >= config['daily_max']:
        exp,bean = 0.0, 0.0

    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'], talent-maxtalent,config['module']['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, config['module']['talent']['component_ratio'])

def playsoundoffline(config, data):
    exp, bean, talent = get_value(config, data)
    texp, tbean = get_and_update_one_day_total_exp_and_bean_by_metaid(data, exp, bean)
    if texp > config['module']['exp']['max_value']:
        exp = config['module']['exp']['exceed_value']
    if tbean > config['module']['mua_bean']['max_value']:
        bean = config['module']['mua_bean']['exceed_value']

    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'], talent-maxtalent,config['module']['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, config['module']['talent']['component_ratio'])

def playnote(data, config):
    if data['meta'].get('is_ordered', False) == True:
        c = config['ordered']
    else:
        c = config['unordered']

    exp = c['exp']['value']*data['value']
    talent = c['talent']['value']*data['value']
    bean = c['mua_bean']['value']*data['value']
    count = get_and_update_one_day_times(data)
    if count > 0:
        d = math.pow(config['time_decrease']['percentage_decrease'], count)
        exp = exp * d
        bean = bean * d
        if exp < config['time_decrease']['min_value']:
            exp = config['time_decrease']['min_value']
        if bean < config['time_decrease']['min_value']:
            bean = config['time_decrease']['min_value']

    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'],talent-maxtalent,c['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, c['talent']['component_ratio'])
        
def playdj(data, config):
    if 'total' in data['meta']:
        pass
    else:
        return
    exp = config['exp']['value']*data['value']*data['meta']['total']
    bean = config['bean']['value']*data['value']*data['meta']['total']
    talent = config['talent']['value']*data['value']*data['meta']['total'] 

    count = get_and_update_one_day_times(data)
    # TODO > or >=
    if count > config['exp']['max_times']:
        exp = config['exp']['exceed_value']
        bean = config['bean']['exceed_value']

    maxtalent = get_pbrecord_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_pbrecord_max_talent(data, talent)
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'],talent-maxtalent,config['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, config['talent']['component_ratio'])

def dailytimedecrease(data, config):
    global debug
    exp = config['exp']['value']*data['value']
    bean = config['mua_bean']['value']*data['value']
    talent = config['talent']['value']*data['value']

    count = get_and_update_one_day_module_times(data)
    starttimes = config.get('start_time', 0)
    if count > starttimes:
        ed = math.pow(config['exp']['percentage_decrease'], count - starttimes)
        bd = math.pow(config['mua_bean']['percentage_decrease'], count - starttimes)
        exp = exp * ed
        bean = bean * bd
        if exp < config['exp']['min_value']:
            exp = config['exp']['min_value']
        if bean < config['mua_bean']['min_value']:
            bean = config['mua_bean']['min_value']
    maxtalent = get_pbmodule_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'],exp,bean, data['created_at']['$numberLong'])
    else:
        update_user_property(data,data['uid']['$numberLong'],exp,bean,data['created_at']['$numberLong'], talent-maxtalent,config['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, config['talent']['component_ratio'])


def dailytotallimit(data, config):
    exp = config['exp']['value']*data['value']
    bean = config['mua_bean']['value']*data['value']
    talent = config['talent']['value']*data['value']

    texp, tbean = get_and_update_one_day_total_exp_and_bean_by_module_id(data, exp, bean)
    if texp > config['exp']['max_value']:
        exp = config['exp']['exceed_value']
    if tbean > config['mua_bean']['max_value']:
        bean = config['mua_bean']['exceed_value']
    maxtalent = get_pbmodule_max_talent(data)
    if maxtalent >= talent:
        update_user_property(data,data['uid']['$numberLong'], exp, bean, data['created_at']['$numberLong'])
    else:
        update_user_property(data,data['uid']['$numberLong'], exp, bean, data['created_at']['$numberLong'], talent-maxtalent,config['talent']['component_ratio'])
        generate_pbmoduletalents_file(data, talent-maxtalent, config['talent']['component_ratio'])

def getconfig():
    global config, maxidcount
    with open(id_file, 'r') as f:
        allline = f.read()
        for line in allline.splitlines():
            if 'uc.pbmoduletalents' in line:
                line = json.loads(line)
                maxidcount = line['offset']


    configall = json.loads(open(etcd_file, 'r').read())
    func={}
# level config
    config['level'] = configall['score_config']['level_exp_gradient']
# music radio
    for c in configall['score_config']['music_radio_configs']:
        func[c['module_id']] = musicradio
        config[c['module_id']] = c

# play sound
    for c in configall['score_config']['play_sound_configs']:
        func[c['module_id']] = playsound
        config[c['module_id']] = c

# play note
    for c in configall['score_config']['play_note_configs']:
        func[c['module_id']] = playnote
        config[c['module_id']] = c

# play dj
    for c in configall['score_config']['play_dj_configs']:
        func[c['module_id']] = playdj
        config[c['module_id']] = c

# daily total limit
    for c in configall['score_config']['daily_total_limit_modules']:
        func[c['module_id']] = dailytotallimit
        config[c['module_id']] = c
    
    for c in configall['score_config']['daily_times_decrease_modules']:
        for c1 in c['modules_id']:
            func[c1] = dailytimedecrease
            config[c1] = c

    return func, config

def nested_dict():
    return defaultdict(nested_dict)

def get_value(config, data):
    eValue = config['module']['exp']['value']
    mValue = config['module']['mua_bean']['value']
    tValue = config['module']['talent']['value']
    exp, bean, talent = eValue*data['value'], mValue*data['value'], tValue*data['value']
    return exp, bean, talent

def if_tow_time_in_one_day(time):
    global day_flag, pb_metaid_count, pb_moduleid_count, pb_oneday_metaid_total,pb_oneday_moduleid_total 
    if day_flag//86400000000000 == time//86400000000000:
        return True
    else:
        while True:
            day_flag = day_flag+86400000000000 
            if day_flag//86400000000000 == time//86400000000000:
                break
        pb_metaid_count.clear()
        pb_moduleid_count.clear()
        pb_oneday_metaid_total.clear()
        pb_oneday_moduleid_total.clear() 
        return False

def update_user_property(data,uid, exp, bean, created_at, talent=0.0, component_ratio=[0,0,0,0,0]):
    global debug
    if str(debug) == uid:
        e = int(data['created_at']['$numberLong'][:10])
        e = datetime.datetime.fromtimestamp(e).strftime('%Y-%m-%d')
        moduleid = data['module_id']['$numberLong']
        recordid = data['_id']['$numberLong']
        systalent = data['talent']
        sysexp = data['exp']
        sysbean = data['mua_bean']
        print 'my', recordid, talent, exp, bean
        print 'sys', recordid, systalent, sysexp, sysbean
        print recordid, uid, moduleid, talent-systalent, exp-sysexp, bean-sysbean

    global user_property
    if exp == 0 and bean == 0 and talent == 0 and component_ratio == [0,0,0,0,0]:
        return
# test
    user = user_property.get(uid, {}).get('data', [0,0,0,0,0,0,0,0])
    user[0] += exp
    user[1] += bean
    user[2] += talent
    user[3] += talent*component_ratio[0]
    user[4] += talent*component_ratio[1]
    user[5] += talent*component_ratio[2]
    user[6] += talent*component_ratio[3]
    user[7] += talent*component_ratio[4]
    if uid in user_property:
        user_property[uid]['updated_at'] = created_at
    else:
        user_property[uid]['updated_at'] = created_at
        user_property[uid]['created_at'] = created_at

    user_property[uid]['data'] = user

def get_pbrecord_max_talent(data):
    global pbrecord_max_talent
    maxtalent = pbrecord_max_talent.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], {}).get(data['meta']['id'], 0)
    return maxtalent

def update_pbrecord_max_talent(data, talent):
    global pbrecord_max_talent
    pbrecord_max_talent[data['uid']['$numberLong']][data['module_id']['$numberLong']][data['meta']['id']] = talent

def get_pbmodule_max_talent(data):
    global pbmodule_max_talent
    a = pbmodule_max_talent.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], 0)
    return a

def update_pbmodule_max_talent(data, talent):
    global pbmodule_max_talent
    pbmodule_max_talent[data['uid']['$numberLong']][data['module_id']['$numberLong']] = talent

def get_and_update_one_day_times(data):
    global pb_metaid_count
    in_one_day = if_tow_time_in_one_day(int(data['created_at']['$numberLong']))

    count = pb_metaid_count.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], {}).get(data['meta']['id'], 0)
    pb_metaid_count[data['uid']['$numberLong']][data['module_id']['$numberLong']][data['meta']['id']] = count + 1
    return count

def get_and_update_one_day_module_times(data):
    global pb_moduleid_count
    in_one_day = if_tow_time_in_one_day(int(data['created_at']['$numberLong']))

    count = pb_moduleid_count.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], 0)
    pb_moduleid_count[data['uid']['$numberLong']][data['module_id']['$numberLong']] = count + 1
    return count

def get_and_update_one_day_total_exp_and_bean_by_metaid(data, exp, bean):
    global pb_oneday_metaid_total
    in_one_day = if_tow_time_in_one_day(int(data['created_at']['$numberLong']))

    print(data)
    texp = pb_oneday_metaid_total.get(data['uid']['$numberLong'], {}).\
            get(data['module_id']['$numberLong'], {}).get(data['meta']['id'], {}).get('exp', 0)
    tbean = pb_oneday_metaid_total.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], {}).get(data['meta']['id'], {}).get('bean', 0)

    pb_oneday_metaid_total[data['uid']['$numberLong']][data['module_id']['$numberLong']][data['meta']['id']]['exp'] = texp + exp
    pb_oneday_metaid_total[data['uid']['$numberLong']][data['module_id']['$numberLong']][data['meta']['id']]['bean'] = tbean + bean
    return texp, tbean

def get_and_update_one_day_total_exp_and_bean_by_module_id(data, exp, bean):
    global pb_oneday_moduleid_total
    in_one_day = if_tow_time_in_one_day(int(data['created_at']['$numberLong']))

    texp = pb_oneday_moduleid_total.get(data['uid']['$numberLong'], {}).\
            get(data['module_id']['$numberLong'],{}).get('exp', 0)
    tbean = pb_oneday_moduleid_total.get(data['uid']['$numberLong'], {}).get(data['module_id']['$numberLong'], {}).get('bean', 0)

    pb_oneday_moduleid_total[data['uid']['$numberLong']][data['module_id']['$numberLong']]['exp'] = texp + exp
    pb_oneday_moduleid_total[data['uid']['$numberLong']][data['module_id']['$numberLong']]['bean'] = tbean + bean
    return texp, tbean

def generate_pbmoduletalents_file(data, incrtalent, component_ratio):
    global offset
    maxtalent = get_pbmodule_max_talent(data)
    talent = maxtalent + incrtalent
    update_pbmodule_max_talent(data, talent)

    w = nested_dict()
    if offset > maxidcount:
        print 'no id can be use!'
        return
    w['_id']['$numberLong'] = str(offset)
    offset += 1
    w['pb_play_record_id']['$numberLong'] = data['_id']['$numberLong']
    w['uid']['$numberLong'] = data['uid']['$numberLong']
    w['module_id']['$numberLong'] = data['module_id']['$numberLong']
    w['talent'] = talent
    w['talent_component']['appreciationing'] = talent * component_ratio[0]
    w['talent_component']['rhythming'] = talent * component_ratio[1]
    w['talent_component']['listening'] = talent * component_ratio[2]
    w['talent_component']['creativing'] = talent * component_ratio[3]
    w['talent_component']['expressioning'] = talent * component_ratio[4]
    w['created_at']['$numberLong'] = data['created_at']['$numberLong']
    w['updated_at']['$numberLong'] = data['created_at']['$numberLong']

    with open(module_file, 'w') as f:
        json.dump(w, f, separators=(',', ':'))
        f.write('\n')

def calc_user_level(exp):
    global config
    for index, item in enumerate(config['level']):
        if exp < item:
            return index
    return index + 1

def generate_userproperty_file(data):
    with open(user_file, 'w') as f:
        for k,v in data.items():
            user = nested_dict()
            user['_id']['$numberLong'] = k
            user['level'] = calc_user_level(v['data'][0])
            user['experience_total'] = v['data'][0]
            user['talent_total'] = v['data'][2]
            user['talent_component_total']['appreciationing'] = v['data'][5]
            user['talent_component_total']['rhythming'] = v['data'][3]
            user['talent_component_total']['listening'] = v['data'][6]
            user['talent_component_total']['creativing'] = v['data'][7]
            user['talent_component_total']['expressioning'] = v['data'][4]
            user['mua_bean_total'] = v['data'][1]
            user['updated_at']['$numberLong'] = v['updated_at']
            user['created_at']['$numberLong'] = v['created_at']
            json.dump(user, f, separators=(',', ':'))
            f.write('\n')

def if_inter_user(r):
    global inter_user
    if str(r['uid']['$numberLong']) in inter_user:
        return True
    else:
        return False

def main():
    global pbrecord_max_talent, pbmodule_max_talent, pb_metaid_count, pb_moduleid_count, pb_oneday_metaid_total, pb_oneday_moduleid_total, user_property, debug, inter_user
    inter_user = ('1357083804530935340', '1482208423076219372', '1495913840485562740', '15575927634607576', '1715996617512634332','1883957127547848811', '205', '25918507571488141', '314743263722352156', '669721402775461212', '688100081261295428', '797675498430224443', '932450267735279749', '1858792661077192107', '1', '292936401541694168', '183852843261767282', '1207466094979917770', '1714843094412090421', '1057967653400425841', '1240979002236083387', '808333249199325520', '2026440252271029645')
    pbrecord_max_talent = nested_dict()
    pbmodule_max_talent = nested_dict()
    pb_metaid_count = nested_dict()
    pb_moduleid_count = nested_dict()
    pb_oneday_metaid_total = nested_dict()
    pb_oneday_moduleid_total = nested_dict()
    user_property = nested_dict()

    if len(sys.argv) == 2:
        debug = sys.argv[1]
        print debug
    getfile()
    fMap, cMap = getconfig()
    with open(pbr_file, 'r') as f:
        all_pbrecord_line = f.read()
        for r in all_pbrecord_line.splitlines():
            r = json.loads(r)
            flag = if_inter_user(r)
            if flag:
                continue
            if len(sys.argv) == 2 and sys.argv[1] != r['uid']['$numberLong']:
                continue
            f = fMap[int(r['module_id']['$numberLong'])]
            f(r, cMap[int(r['module_id']['$numberLong'])])
                
    generate_userproperty_file(user_property)

main()
