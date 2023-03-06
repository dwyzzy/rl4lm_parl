from typing import Any, Dict, Type, Union

import parl
from benchmark.torch.RL4LMs.algorithms import RL4LMPPO
from benchmark.torch.RL4LMs.agents import RL4LMsAgent

from benchmark.torch.RL4LMs.utils  import TextGenPool, CNNDailyMail
# from rl4lms.envs.text_generation.alg_wrappers import wrap_onpolicy_alg
from parl.utils import logger

from benchmark.torch.RL4LMs.metrics import (
    BaseMetric,
    BERTScoreMetric,
    BLEUMetric,
    BLEURTMetric,
    BLEUToTTo,
    DiversityMetrics,
    LearnedRewardMetric,
    MeteorMetric,
    Perplexity,
    RougeLMax,
    RougeMetric,
    SacreBLEUMetric,
    TERMetric,
    chrFmetric,
)

from benchmark.torch.RL4LMs.models import Seq2SeqLMModel

from benchmark.torch.RL4LMs.utils import (
    BERTScoreRewardFunction,
    BLEURewardFunction,
    BLEURTRewardFunction,
    CommonGenPenaltyShapingFunction,
    LearnedRewardFunction,
    MeteorRewardFunction,
    RewardFunction,
    RougeCombined,
    RougeLMaxRewardFunction,
    RougeRewardFunction,
    SacreBleu,
)



class DataPoolRegistry:
    _registry = {
        "cnn_daily_mail": CNNDailyMail,
    }

    @classmethod
    def get(cls, datapool_id: str, kwargs: Dict[str, Any]) -> TextGenPool:
        logger.info(f"loading split of dataset: {datapool_id} -- {kwargs['split']}")
        datapool_cls = cls._registry[datapool_id]
        datapool = datapool_cls.prepare(**kwargs)
        return datapool

    @classmethod
    def add(cls, id: str, datapool_cls: Type[TextGenPool]):
        DataPoolRegistry._registry[id] = datapool_cls


class RewardFunctionRegistry:
    _registry = {
        "learned_reward": LearnedRewardFunction,
        "meteor": MeteorRewardFunction,
        "rouge": RougeRewardFunction,
        "bert_score": BERTScoreRewardFunction,
        "bleu": BLEURewardFunction,
        "bleurt": BLEURTRewardFunction,
        "rouge_combined": RougeCombined,
        "common_gen_repeat_penalty": CommonGenPenaltyShapingFunction,
        "sacre_bleu": SacreBleu,
        "rouge_l_max": RougeLMaxRewardFunction,
    }

    @classmethod
    def get(cls, reward_fn_id: str, kwargs: Dict[str, Any]) -> RewardFunction:
        logger.info(f"loading reward function: {reward_fn_id}")
        reward_cls = cls._registry[reward_fn_id]
        reward_fn = reward_cls(**kwargs)
        return reward_fn

    @classmethod
    def add(cls, id: str, reward_fn_cls: Type[RewardFunction]):
        RewardFunctionRegistry._registry[id] = reward_fn_cls


class MetricRegistry:
    _registry = {
        "learned_reward": LearnedRewardMetric,
        "meteor": MeteorMetric,
        "rouge": RougeMetric,
        "bert_score": BERTScoreMetric,
        "bleu": BLEUMetric,
        "bleurt": BLEURTMetric,
        "diversity": DiversityMetrics,

        "causal_perplexity": Perplexity,

        "bleu_totto": BLEUToTTo,
        "rouge_l_max": RougeLMax,
        "sacre_bleu": SacreBLEUMetric,
        "ter": TERMetric,
        "chrf": chrFmetric,

    }

    @classmethod
    def get(cls, metric_id: str, kwargs: Dict[str, Any]) -> BaseMetric:
        logger.info(f"loading metric: {metric_id}")
        metric_cls = cls._registry[metric_id]
        metric = metric_cls(**kwargs)
        return metric

    @classmethod
    def add(cls, id: str, metric_cls: Type[BaseMetric]):
        MetricRegistry._registry[id] = metric_cls


class ModelRegistry:
    _registry = {
        "seq2seq_lm_actor_critic_model": Seq2SeqLMModel,
    }

    @classmethod
    def get(cls, model_id: str) -> Type[parl.Model]:
        model_cls = cls._registry[model_id]
        return model_cls


class AlgorithmRegistry:
    _registry = {
        "ppo": RL4LMPPO,
    }

    @classmethod
    def get(
        cls, alg_id: str
    ):
        try:
            alg_cls = cls._registry[alg_id]
        except KeyError:
            raise NotImplementedError
        return alg_cls

    @classmethod
    def add(
        cls, id: str, alg_cls
    ):
        AlgorithmRegistry._registry[id] = alg_cls


class AgentRegistry:
    _registry = {
        "rl4lm_agent": RL4LMsAgent,
    }

    @classmethod
    def get(cls, alg_id: str):
        try:
            wrapper_def = cls._registry[alg_id]
        except KeyError:
            raise NotImplementedError
        return wrapper_def

    @classmethod
    def add(cls, id: str, agent_def):
        AgentRegistry._registry[id] = agent_def

