# Voice Passing：用于评估跨性别声音转换的非二元声音性别预测系统

David Doukhan, Simon Devauchelle, Lucile Girard-Monneron, Mía Chávez Ruz, V. Chaddouk, Isabelle Wagner, Albert Rilliard

Proc. INTERSPEECH 2023, 5207-5211

[eess.AS] [HCI] [ML] [Audio] [PR] [Data] [AI system]

2024年04月23日

-   [简介](#introduction)
-   [图表](#charts)
-   [解决问题](#problem_solved)
-   [关键思路](#key_ideas)
-   [其它亮点](#other_highlights)
-   [相关研究](#related_research)

## 简介

本文介绍了一种软件，可以使用连续的声音女性化百分比（VFP）来描述声音。该系统旨在为跨性别者在声音转换过程中和支持他们的语音治疗师使用。记录了41位法国的顺性别和跨性别者的语料库。通过感知评估，57名参与者估计了每个声音的VFP。在外部性别平衡数据上训练了二元性别分类模型，并在重叠窗口上使用，以获得平均性别预测估计值，这些估计值被校准以预测VFP，并比基于$F\_0$或声道长度的模型获得更高的准确性。训练数据的说话风格和DNN架构被证明会影响VFP的估计。模型的准确性受到说话者年龄的影响。这凸显了风格、年龄以及将性别概念视为二元或非二元的重要性，以建立足够的文化概念的统计表示。

## 图表

-   ![](https://simg.baai.ac.cn/papers/converted_page_1cab1c39f95e8a0ef53164aa0ce12c56-01.jpg)

## 解决问题

本文旨在提出一种连续的声音女性化百分比（VFP）描述方法，以帮助跨性别者进行声音转换，同时为支持他们的声音治疗师提供帮助。研究的重点是如何建立一个准确的VFP预测模型。

## 关键思路

通过使用外部平衡性别数据训练二元性别分类模型，并在重叠窗口上使用这些模型来获得平均性别预测估计值，然后校准以预测VFP，从而提高模型的准确性。

## 其它亮点

本文使用了41个法语跨性别者和非跨性别者的语音语料库，并进行了感知评估。实验结果表明，训练数据的语音风格和DNN架构会影响VFP估计的准确性。此外，模型的准确性还受到说话者年龄的影响。本文的方法可以为跨性别者的声音治疗提供指导，并为研究跨性别声音转换提供新思路。

## 相关研究

最近的相关研究包括：1. “A Deep Learning Approach to Gender Classification of Euphonious Speech”；2. “Voice Conversion for Transgender Speakers with Non-Parallel Corpora Using Variational Autoencoder and Multi-Encoder”；3. “A Review of Voice Conversion Techniques for Non-Parallel Corpora”等。
