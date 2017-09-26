import torch
import os, argparse
from srcnn import SRCNN
from vdsr import VDSR

"""parsing and configuration"""
def parse_args():
    desc = "Pytorch implementation of SR collections"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--model_name', type=str, default='VDSR',
                        choices=['SRCNN', 'VDSR', 'DRCN', 'ESPCN', 'FastNeuralStyle', 'FSRCNN', 'SRResNet', 'LapSRN', 'EnhanceNet', 'EDSR', 'EnhanceGAN'], help='The type of model')
    parser.add_argument('--data_dir', type=str, default='../Data')
    parser.add_argument('--dataset', type=str, default='bsds300', choices=['bsds300', 'fashion-mnist', 'celebA'],
                        help='The name of dataset')
    parser.add_argument('--num_threads', type=int, default=4, help='number of threads for data loader to use')
    parser.add_argument('--num_channels', type=int, default=1, help='The number of channels to super-resolve')
    parser.add_argument('--scale_factor', type=int, default=2, help='Size of scale factor')
    parser.add_argument('--num_epochs', type=int, default=80, help='The number of epochs to run')
    parser.add_argument('--batch_size', type=int, default=64, help='training batch size')
    parser.add_argument('--test_batch_size', type=int, default=10, help='testing batch size')
    parser.add_argument('--save_dir', type=str, default='Result', help='Directory name to save the results')
    parser.add_argument('--lr', type=float, default=0.1)
    parser.add_argument('--gpu_mode', type=bool, default=True)

    return check_args(parser.parse_args())

"""checking arguments"""
def check_args(args):
    # --save_dir
    args.save_dir = os.path.join(args.save_dir, args.model_name)
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    # --epoch
    try:
        assert args.num_epochs >= 1
    except:
        print('number of epochs must be larger than or equal to one')

    # --batch_size
    try:
        assert args.batch_size >= 1
    except:
        print('batch size must be larger than or equal to one')

    return args

"""main"""
def main():
    # parse arguments
    args = parse_args()
    if args is None:
            exit()

    if args.gpu_mode and not torch.cuda.is_available():
        raise Exception("No GPU found, please run without --gpu_mode=False")

    # model
    if args.model_name == 'SRCNN':
        net = SRCNN(args)
    elif args.model_name == 'VDSR':
        net = VDSR(args)
    # elif args.model_name == 'DRCN':
    #     net = DRCN(args)
    # elif args.model_name == 'ESPCN':
    #     net = ESPCN(args)
    # elif args.model_name == 'FastNeuralStyle':
    #     net = FastNeuralStyle(args)
    # elif args.model_name == 'FSRCNN':
    #     net = FSRCNN(args)
    # elif args.model_name == 'SRResNet':
    #     net = SRResNet(args)
    # elif args.model_name == 'LapSRN':
    #     net = LapSRN(args)
    # elif args.model_name == 'EnhanceNet':
    #     net = EnhanceNet(args)
    # elif args.model_name == 'EDSR':
    #     net = EDSR(args)
    # elif args.model_name == 'EnhanceGAN':
    #     net = EnhanceGAN(args)
    else:
        raise Exception("[!] There is no option for " + args.model_name)

    # train
    net.train()

    # test
    model_dir = os.path.join(args.save_dir, 'model')
    saved_model = model_dir + '/' + args.model_name + '_param.pkl'
    net.test(saved_model)

if __name__ == '__main__':
    main()