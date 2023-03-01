import os
from argparse import ArgumentParser

import yaml
import collections
from trainers import OnPolicyTrainer
from utils import Tracker


def recursive_dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = recursive_dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def main(config):

    # load tracker
    tracker = Tracker(
        config["base_path_to_store_results"],
        config,
        config["project_name"],
        config["experiment_name"],
        config["entity_name"],
        False,
    )

    # instantiate the trainer here
    # TODO: currently only complete ppo
    if "ppo" == config["alg"]["id"]:
        trainer = OnPolicyTrainer(
            tokenizer_config=config["tokenizer"],
            datapool_config=config["datapool"],
            reward_config=config["reward_fn"],
            env_config=config["env"],
            on_policy_alg_config=config["alg"],
            train_eval_config=config["train_evaluation"],
            tracker=tracker,
        )
    else:
        raise NotImplementedError
    trainer.train_and_eval()






if __name__ == '__main__':
    parser = ArgumentParser(description="Fine-tune LM to generate controlled text")
    parser.add_argument("--config_path", type=str, help="path to the config file")
    parser.add_argument(
        "--project_name", type=str, help="project name", default="rl4lm_exps"
    )
    parser.add_argument(
        "--experiment_name",
        type=str,
        help="experiment name",
        default="rl4lm_experiment",
    )
    parser.add_argument(
        "--base_path_to_store_results",
        type=str,
        help="Base path to store experiment results",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    # load the config file
    with open(args.config_path, "r") as fp:
        config = yaml.safe_load(fp)

    recursive_dict_update(config, args)

    main(config)

