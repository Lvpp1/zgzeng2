import logging,requests,os,pathlib


requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('my_logger')

company_path = os.path.join(pathlib.Path(__file__).parent.parent, 'company')



def get_unit():
    """获取所有单位名称,存放在列表中"""
    result = []
    try:
        with open(company_path, 'r', encoding='utf8') as fh:
            contents = fh.readlines()
        for item in contents:
            if '-' in item:
                result.append(item.split('-')[1].replace('\n', ''))
            elif '\n' in item:
                result.append(item.replace('\n', ''))
            else:
                result.append(item)
        return result
    except Exception as e:
        logger.error(f'error - {e}')