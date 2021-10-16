import subprocess, argparse, os, stat, shutil, re

# Definition constant
LMP_PATH = '/program/lammps201029/build/lmp'

# 環境変数の設定
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['OMPI_ALLOW_RUN_AS_ROOT'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'  

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, default='/opt/ml/processing/input/')
    parser.add_argument('--input-equiliv-in', type=str, default='lmp_equiliv.in')
    parser.add_argument('--input-equiliv-sh', type=str, default='lmp_equiliv.sh')
    parser.add_argument('--input-lmp2data-py', type=str, default='lmp2data.py')
    parser.add_argument('--np', type=str, default='1')
    parser.add_argument('--gpu', type=str, default='1')
    parser.add_argument('--output-dir', type=str, default='/opt/ml/processing/output')
    parser.add_argument('--logfile-name', type=str, default='lmp_equiliv.log')
    args, _ = parser.parse_known_args()
    print(f'Received arguments {args}')
    return args

if __name__=='__main__':
    args = parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    logfile_name = args.logfile_name
    logfile_tmp_path = os.path.join(input_dir,logfile_name)
    logfile_path = os.path.join(output_dir,logfile_name)
    
    # デフォルトだとカレントディレクトリは root であり、
    # mpirunに都合が悪いのでファイル群が置いてあるinput_dir(/opt/ml/processing/input)に移動
    # cd /opt/ml/processing/input/
    # ※このコードは/opt/ml/processing/input/code/以下にある
    print('change directory')
    os.chdir(input_dir)
    
    print('check current directory')
    cmd_response = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cmd_response.stdout.decode())
        
    print('mpi will be started with following command.')
    command = f'bash {args.input_equiliv_sh} {args.np} {args.gpu} {LMP_PATH} {args.input_equiliv_in} {logfile_tmp_path}'
    command_list = command.split(' ')
    print(*command_list)
    cmd_response = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # mpirun を走らせると大量の標準エラー出力が出るので、ダンプして output_dir に置く(併せて標準出力も)
    # output_dir(/opt/ml/processing/output/) に置くと処理が完了したあと自動的に S3 に転送される
    with open(os.path.join(output_dir,'mpirun_stdout.txt'),mode='w') as f:
        f.write(cmd_response.stdout.decode())
    with open(os.path.join(output_dir,'mpirun_stderr.txt'),mode='w') as f:
        f.write(cmd_response.stderr.decode())
    
    # mpirun が成功したかどうかをログファイルを読んで出力する
    with open('./lmp_equiliv.log') as f:
        print(f.read())
    print('finished mpirun.\n\n')

    # mpirun を実行して生成されるファイルを output_dir にコピーしておく
    for file_name in ['lmp_equiliv.lammpstrj','lmp_equiliv.log','log.cite','log.lammps']:
        shutil.copy2(os.path.join(input_dir,file_name), output_dir)
    
    # lmp_equiliv.logに含まれる表をcsv形式にして別途出力
    with open(os.path.join(output_dir,'lmp_equiliv.log'),'r')  as f:
        text = f.read()
        text_list = text.split('\n')
    header = 'Step Time Temp PotEng KinEng TotEng Enthalpy Press Volume Density '
    footer_list=[header for header in text_list if header.startswith('Loop time')]
    for counter in range(text_list.count(header)):
        index = (text_list.index(header),text_list.index(footer_list[counter]))
        extract_text = text_list[index[0]:index[1]]
        csv_txt = ""
        for t in text_list[index[0]:index[1]]:
            tmp = re.sub('[ 　]+', ',', t)
            if tmp[0]==',':
                tmp=tmp[1:]
            if tmp[-1]==',':
                tmp=tmp[:-1]
            tmp+='\n'
            csv_txt += tmp
        csv_txt = csv_txt[:-1]
        with open(os.path.join(output_dir,f'{str(counter)}.csv'),'w') as f:
            f.write(csv_txt)
        text_list=text_list[index[1]:]
    
    
    # lmp2data.py を実行
    print('exec lmp2data.py with following command.')
    command = f'python {args.input_lmp2data_py} equiliv'
    command_list = command.split(' ')
    print(*command_list)
    cmd_response = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print('finished lmp2data.py.\n\n')
    
    # lmp2data.py の結果をテキストファイルに書き込み
    with open(os.path.join(output_dir,'lmp2data_stdout.txt'),mode='w') as f:
        f.write(cmd_response.stdout.decode())
    with open(os.path.join(output_dir,'lmp2data_stderr.txt'),mode='w') as f:
        f.write(cmd_response.stderr.decode())
    
    # 併せて標準出力(Notebookの出力とCloudWatch Logsへ書き込み)
    print('stdout:')
    print('    ' + cmd_response.stdout.decode())
    
    exit()