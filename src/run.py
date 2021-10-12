import subprocess, argparse, os, stat

# Definition constant
LOGFILE_NAME = 'lmp_equiliv.log'
LMP_PATH = '/program/lammps201029/build/lmp'

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
    logfile_path = os.path.join(args.output_dir,LOGFILE_NAME)
    
    # cd /opt/ml/processing/input/
    os.chdir(input_dir)
    
    # chmod lmp_equiliv.sh +x
#     os.chmod(f'./{args.input_equiliv_sh}',  0o777) 
    
    
    cmd_response = subprocess.run(["ls", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cmd_response.stdout.decode())
    
#     cmd_response = subprocess.run(['which','bash'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     print(cmd_response.stdout.decode())
    
#     cmd_response = subprocess.run(["ls", "-l", "/usr/bin/bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     print(cmd_response.stdout.decode())
    
    cmd_response = subprocess.run(["cat", args.input_equiliv_sh], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(cmd_response.stdout.decode())

    
    
    command = f'bash {args.input_equiliv_sh} {args.np} {args.gpu} {LMP_PATH} {args.input_equiliv_in} {logfile_path} {args.input_lmp2data_py}'
    command_list = command.split(' ')

    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    os.environ['OMPI_ALLOW_RUN_AS_ROOT'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    
    
    
#     command = f'mpirun --allow-run-as-root -np {args.np} {LMP_PATH} -sf gpu -pk gpu {args.gpu} -in {args.input_equiliv_in}'
#     command_list = command.split(' ')
    print('mpi will be started...')
    print(command_list)
    cmd_response = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print('mpi ended...')
    print(cmd_response.stdout.decode())
    print(cmd_response.stderr.decode())
    