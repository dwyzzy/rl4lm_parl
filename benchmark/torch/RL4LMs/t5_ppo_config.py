
config = {
    'tokenizer': {
        'model_name': 't5-base',
        'padding_side': 'left',
        'truncation_side': 'left',
        'pad_token_as_eos_token': False
    },
    'datapool': {
        'id': 'cnn_daily_mail',
        'args': {
            'prompt_prefix': 'Summarize: '
        }
    },
    'instructor': {
        'parl_master_address': 'localhost:8811',
        'n_instructors': 100,
        'reward_fn': {
            'args': {
                'rouge_type': 'rouge1'
            }
        },
        'args': {
            'max_prompt_length': 512,
            'max_episode_length': 100,
            'terminate_on_eos': True,
            'prompt_truncation_side': 'right',
            'context_start_token': 0
        }
    },
    'kl_div': {
        'coeff': 0.001,
        'target_kl': 0.2
    },
    'rollout_buffer': {
        'args': {
            'n_steps_per_episode': 512  # buffer length = n_steps_per_episode * n_instructors
        }
    },
    'agent': {
        'args': {
            'batch_size': 32,
            'n_epochs': 5
        },
        'alg': {
            'args': {
                'initial_lr': 0.000002,
                'entropy_coef': 0.0
            },
            'model': {
                'args': {
                    'model_name': 't5-base',
                    'apply_model_parallel': True,
                    'prompt_truncation_side': 'right',
                    'generation_kwargs': {
                        'do_sample': True,
                        'top_k': 50,
                        'min_length': 50,
                        'max_new_tokens': 100
                    }
                }
            }
        }
    },
    'examiner': {
        'args': {
            'max_prompt_length': 512,
            'eval_batch_size': 100,
            'generation_kwargs': {
                'do_sample': True,
                'top_k': 0,
                'temperature': 0.7,
                'min_length': 50,
                'max_new_tokens': 100
            }
        },
        'metrics': [
            {
                'id': 'meteor',
                'args': {}
            }, {
                'id': 'rouge'
            }, {
                'id': 'bleu',
                'args': {}
            }, {
               'id': 'bert_score',
               'args': {
                'language': 'en'
               }
            }, {
                'id': 'diversity',
                'args': {}
            }
        ]
    },
    'train_evaluation': {
        'n_iters': 100,
        'eval_every': 10
    }
}
