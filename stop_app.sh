#!/bin/bash
ps -ef | grep "NPC_Backend" | grep -v grep | awk '{print $2}' | xargs kill -9 
