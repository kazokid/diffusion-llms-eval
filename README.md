# Comparison of autoregressive and discrete diffusion language models in planning and reasoning oriented tasks


The development of Large Language Models (LLMs) has mostly been based on the autoregressive (AR)
paradigm, which generates text sequentially in a left-to-right manner. Discrete diffusion models have recently
emerged as an alternative approach, enabling bidirectional context integration and iterative denoising. The
introduction of remasking sampling strategies allows controlled resampling of uncertain tokens. Unlike AR
models, which may propagate early generation errors, remasking diffusion-based models allow for the
correction of errors in later denoising steps. The objective of this master's thesis is to investigate and compare
three architectural paradigms, autoregressive models, standard discrete diffusion models, and diffusion models
employing a remasking sampling mechanism, in the context of planning and reasoning tasks. Compared
models will be of similar parameter sizes. The research will include the preparation of appropriate planning and
reasoning benchmarks, selection and configuration of the three models, implementation of the resampling
strategy, and a comparative analysis based on determined evaluation criteria. Evaluation criteria will include the
accuracy rate on selected planning benchmarks and a qualitative assessment of the strengths and limitations of
each architectural paradigm. The assessment aims to provide recommendations regarding the applicability of
remasking diffusion models in agent-oriented planning scenarios. The final documentation will include a detailed
description of the implemented remasking sampling architecture, accompanied by relevant segments of source
code and technical explanations. The submission will provide the source code, experimental notebooks, and
supplementary documentation.
