import os
import os.path
import win32com.client
import subprocess
import xml.etree.ElementTree as ET
import time
import shutil
from datetime import datetime


class Miscellaneous(object):

    @staticmethod
    def execute_svn_cmd(args):
        p = subprocess.Popen('svn ' + args, stdout=subprocess.PIPE, shell=True)
        print 'Executing command: \'svn ' + args + '\''
        (output, err) = p.communicate()
        print 'Result: \n', output
        if err is not None:
            print 'Error: \n', err

        return output

    @staticmethod
    def process_file(ea_rep, component, eap_file, eap_path):
        if ea_rep is None:
            print 'COM dispatch error: EA.Repository'
        else:
            try:
                ea_rep.OpenFile(eap_path)
            except Exception as e:
                print 'Failed to open eap file: ' + component + ' - ' + eap_file
                print e
                return

        xml_string = ea_rep.SQLQuery("select version from t_diagram where name='CDD Table Of Contents'")
        root = ET.fromstring(xml_string)
        cdd_version = ''
        for version in root.iter("Row"):
            cdd_version = version.find("version").text

        ea_rep.CloseFile()

        if cdd_version is '':
            return component + ';' + eap_file + ';' + 'Can\'t find diagram: CDD Table Of Contents.'
        else:
            return component + ';' + eap_file + ';' + cdd_version

    def get_version_components(self, root):
        directory = 'eap_temp'
        log = 'Component;EAP file name;Version\n'

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if not os.path.isdir(directory):
                    raise e

        ea = win32com.client.Dispatch('EA.Repository')

        component_list = self.execute_svn_cmd('list ' + root)

        component_names = component_list.replace('\r', '').split('\n')
        for cname in component_names:
            cname = cname.strip('/')
            print 'Component: ', cname
            file_list = self.execute_svn_cmd('list ' + root + cname + '/trunk/Design/')
            file_names = file_list.replace('\r', '').split('\n')
            eap_files = []
            for fname in file_names:
                if fname.lower().endswith('.eap'):
                    eap_files.append(fname)

            if len(eap_files) == 0:
                log += cname + ';' + 'CDD eap file not found\n'
            else:
                for f in eap_files:
                    if os.path.exists(directory + '/' + f):
                        os.remove(directory + '/' + f)
                    self.execute_svn_cmd(
                        'export \"' + root + cname + '/trunk/Design/' + f + '\" \"eap_temp/' + f + '\"'
                    )
                    eap_full_path = os.getcwd() + '/eap_temp/' + f
                    log += self.process_file(ea_rep=ea, component=cname, eap_file=f, eap_path=eap_full_path) + '\n'

        shutil.rmtree('eap_temp')

        return log

# ---------------------------------------------------------------------------------------------------------------------#
start_time = datetime.now()
svn_root = 'http://d1dapsvn01/svn/INT_Gen_EPAS_R10/Components/'
check = Miscellaneous()
# time_now = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
with open('result_' + time.strftime('%Y%m%d_%H%M%S', time.gmtime()) + '.csv', 'w') as f:
    result = check.get_version_components(root=svn_root)
    f.write(result)
    f.close()
end_time = datetime.now()
print 'Duration: {}'.format(end_time - start_time)
