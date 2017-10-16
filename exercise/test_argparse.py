"""test argparse package."""
import argparse
import sys

def test(_):
    """for test."""
    print('test function.')

FLAGS = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.register("type", "bool", lambda v: v.lower() == "true")
    parser.add_argument(
        "--model_dir",
        type=str,
        default="",
        help="Base directory fro output models."
    )
    parser.add_argument(
        "--train_steps",
        type=int,
        default=2000,
        help="Number of training steps."
    )

    FLAGS, unparsed = parser.parse_known_args()
    print("{} {}".format(sys.argv[0], unparsed))
    print(FLAGS)
    test(FLAGS)
