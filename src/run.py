import subprocess, argparse, os, stat, shutil

# Definition constant
LOGFILE_NAME = 'lmp_equiliv.log'
LMP_PATH = '/program/lammps201029/build/lmp'

# Set environment variables
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['OMPI_ALLOW_RUN_AS_ROOT'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'  

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, default=None)
    parser.add_argument('--input-tmp-data', type=str, default=None)
    parser.add_argument('--input-equiliv-in', type=str, default=None)
    parser.add_argument('--input-equiliv-sh', type=str, default=None)
    parser.add_argument('--input-lmp2data-py', type=str, default=None)
    parser.add_argument('--np', type=str, default='2')
    parser.add_argument('--gpu', type=str, default='1')
    parser.add_argument('--output-dir', type=str, default=None)
    args, _ = parser.parse_known_args()
    print(f'Received arguments {args}')
    return args

if __name__=='__main__':
    args = parse_args()
    input_dir = args.input_dir
    logfile_tmp_path = os.path.join(args.input_dir,LOGFILE_NAME)
    logfile_path = os.path.join(args.output_dir,LOGFILE_NAME)
    
    # cd /opt/ml/processing/input/
    os.chdir(input_dir)
    
    print('check current directory')
    cmd_response = subprocess.run(["ls", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cmd_response.stdout.decode())
    
    print('mpi will be started with following command.')
    command = f'bash {args.input_equiliv_sh} {args.np} {args.gpu} {LMP_PATH} {args.input_equiliv_in} {logfile_tmp_path}'
    command_list = command.split(' ')
    print(*command_list)
    cmd_response = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(os.path.join(args.output_dir,'dump.txt'),mode='w') as f:
        f.write(cmd_response.stdout.decode())
    print('end.')

    # copy generated files to output directory 
    for file_name in ['lmp_equiliv.lammpstrj','lmp_equiliv.log','log.cite','log.lammps']:
        shutil.copy2(os.path.join(args.input_dir,file_name), args.output_dir)
    
    
    # lmp2data.py exec
    print('exec lmp2data.py with following command.')
    command = f'python {args.input_lmp2data_py} equiliv'
    command_list = command.split(' ')
    print(*command_list)
    cmd_response = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('end.')
    
    # lmp2data.py の結果をテキストファイルに書き込み
    with open(os.path.join(args.output_dir,'stdout.txt'),mode='w') as f:
        f.write(cmd_response.stdout.decode())
    with open(os.path.join(args.output_dir,'stderr.txt'),mode='w') as f:
        f.write(cmd_response.stderr.decode())
    
    # 併せて標準出力(NotebookとCWLへ書き込み)
    print('stdout:')
    print(cmd_response.stdout.decode())
    print('stderr:')
    print(cmd_response.stderr.decode())
    
    exit()