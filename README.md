# OpenScope

Welcome to OpenScope Subnet, where the power of decentralized AI converges with the world of cryptocurrency trading. OpenScope is a revolutionary network that leverages 0xScope's comprehensive cryptocurrency event dataset to train advanced AI models for predicting price movements with unprecedented accuracy.

![frontpage](/doc/assets/frontpage.png)


## Table of Contents

- [OpenScope](#openscope)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Motivation](#Unleashing-the-Power-of-Decentralized-AI-for-Crypto-Trading-with-OpenScope)
  - [Running A Miner](#running-a-miner)
  - [Running A Validator](#running-a-validator)
  <!--
  - [Running A Validator](#running-a-validator)
  - [Launcher Script](#launcher-script)
    - [Using the launcher](#using-the-launcher)
    - [What it does](#what-it-does)
    - [Video tutorial](#video-tutorial)
   -->

## Overview

Visit [OpenScope Website](https://open.0xscope.com/)

In the fast-paced world of cryptocurrency, staying ahead of the game is crucial. Introducing OpenScope, a groundbreaking decentralized AI network that revolutionizes crypto trading like never before.

OpenScope harnesses the power of 0xScope's comprehensive cryptocurrency event dataset to train cutting-edge, event-driven trading models. By leveraging a diverse range of on-chain data, technical analysis, and news events, such as exchange deposits/withdrawals, project collaborations, and influencer signals, OpenScope empowers miners to develop highly performant AI models that predict potential price movements with unparalleled accuracy.

## How OpenScope works

The OpenScope Subnet will have 3 phase, with diffent miner tasks & validator tasks, right now we are in Phase 1.

### Phase 1

Phase 1 will be the beta version of OpenScope, as a cold start we want to OpenScope to be more friendly to participants, the requirements for miners and validators are less intense.

Miners are required to send cryptocurrency trades based on provided live token events.

These trades should be based on the AI trading model trained with the provided history token events.

Validators will calculated each miner's position value based on each miner's trades in each cycle.

These values will used as each miner's performence to assign weights, the higher the value, the higher the weights.

These weights will eventually decide the incentive of each miner, to be sepecificlly the commune token they gets.

### Phase 2

Start from Phase 2, we will officially full utilize the power of the commune network.

The miner services will no longer make trades as they want, miner module will start to take live token events data as inputs and output trades, just like a general AI model.

Validators will still take trades and perform the usual tasks.

### Phase 3

Since phase 3, miner's are require to update their modules in each cycle and no longer need to send trades.

Validators will directly evaluate the module's performence through a set of standards.

This will be the final form of the OpenScope Subnet.

## Motivation

OpenScope - Unleashing the Power of Decentralized AI for Crypto Trading with OpenScope

The network thrives on the symbiotic relationship between miners and validators. Miners utilize 0xScope's rich event data to train sophisticated AI models and generate trading orders based on real-time event inputs. Validators, on the other hand, continuously assess the performance of these models, assigning higher weights to the most successful miners. This dynamic interplay ensures that the best-performing models are consistently rewarded, driving innovation and excellence within the OpenScope ecosystem.

With OpenScope, you can tap into the collective intelligence of a decentralized network, where the brightest minds in AI and crypto converge to create trading strategies that adapt to the ever-evolving market landscape. Join the OpenScope revolution today and experience the future of crypto trading, powered by cutting-edge AI technology and the wisdom of the crowd.

## Prerequisite

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install CommuneX and cli

[Set up Commune](https://communeai.org/docs/installation/setup-commune)

### Get a CommuneX Key

[Key Basics](https://communeai.org/docs/working-with-keys/key-basics)

## Be part of the OpenScope

There are esstentially 2 ways to participant in OpenScope, you can join as a miner, join as a validator, or you can be both!

### Join as a miner

You easily run the miner services in minutes following the tutorials we prepared for you:

[Running A Miner](/doc/Miner.md)

And of course, you have to understand what should a miner do.

#### What should a miner do

Bascially, each miner's will have the ability to send "trades" to our trade services.

These trades is based on 10 different cryptocurrencies (token).

You can check them [here](./doc/Miner.md)

Miners can open positions (open) and close positions (close) based on these tokens.

Each token is independent and all start with the same position size. This means each trading pair contributes to 10% of the total portfolio value at Genesis.

Opening a position can be either going long (1) or going short (-1) (Max 1X Leverage, basically spot but you can short). 

**Example:**

Let's say on Day 0, my total position value starts with 1 USD.

And I have 10 sub-accounts, each account has a 0.1 value (or USD).

And for each sub-account, you can only trade one specific token. 

On Day 0, I only created a $PEPE long position.

On Day 1, casue $PEPE is up 50%, my $PEPE sub-account is now worth 0.15.

As other sub-accounts stay no change (no open position).
My total position value is 1.05 USD, and my current ROI is 5%.

Miner will need to constantly update the positions ([send the trades](/doc/Miner.md#run-the-miner)) and these trades should be based on the live token events.

Miners should also check [what does these event mean](/resources/events.csv)

OpenScope will provide a complete history token events when you first sign up for being a miner. These events are the trainning dataset for miner's event-driving trading model.


### Join as a validator

Validators query trades from our trade services and use these trades to calculate the miners' position value and ROI.

Then validators should use these data to assign weights to each miners.

All of the tasks is written in the validator examples, once you start the process, the code will do everything.

Learn the details:

[Running A Validator](/doc/Validator.md)


