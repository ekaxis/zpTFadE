#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
GNU General Public License v3.0

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

by mopx
'''

from color import Color
from banners import banner

Color.pl('{BR} %s {W}' % banner())

Color.pl('{B} ヽ(´▽`)/ {BC}Hi, friend! {W}')

Color.pl('\n{BO} Amazon Machine Image (AMI){C} (list){W}\n')
Color.pl('\t ● {R}ami-09d95fab7fff3776c{W} - {P}Amazon Linux 2 AMI{W}')
Color.pl('\t ● {R}ami-085925f297f89fce1{W} - {P}Ubuntu Server 18.04 LTS{W}')
Color.pl('\t ● {R}ami-0077ef9ac037e2df6{W} - {P}Centos-7 pke{W}')
Color.pl('\t ● {R}ami-0e5c98cbcc6bb42a4{W} - {P}openSUSE Leap 15.0{W}')
Color.pl('\t ● {R}ami-004418e3c139e4d53{W} - {P}Fedora Coreos 31{W}')

Color.pl('\n {BO}Instance Type{W}\n')
Color.pl('\t INTANCE TYPE\t   vCPUs\tRAM')
Color.pl('\t {R}t2.nano  \t\t{W}{P}1{W}\t\t  {P}0.5{W}')
Color.pl('\t {R}t2.micro \t\t{W}{P}1{W}\t\t  {P}1{W}')
Color.pl('\t {R}t2.small \t\t{W}{P}1{W}\t\t  {P}2{W}')
Color.pl('\t {R}t2.medium\t\t{W}{P}2{W}\t\t  {P}4{W}')
Color.pl('\t {R}t2.large \t\t{W}{P}2{W}\t\t  {P}8{W}')

Color.pl('\n {BO}Security Group{W}\n')
Color.pl('\t Security group ID\t   Security group name\tPORTS')
Color.pl('\t {R}sg-0efcc8890fd19836f\t{W}{P}root{W}\t\t  {P}22/tcp{W}')

Color.pl('\n {BO}Add a tag to your instance{W}\n')

Color.pl(' [root@aws]$ aws {C}ec2{W} create-tags {C}--resources{W} i-5203422c --tags Key=Name,Value=MyInstance')

Color.pl('\n {BO}List your instances{W}\n')

Color.pl(' [root@aws]$ aws {C}ec2{W} describe-instances {C}--filters{W} "Name=instance-type,Values=t2.micro" {C}--query{W} "Reservations[].Instances[].InstanceId"')
Color.pl(' [root@aws]$ aws {C}ec2{W} describe-instances {C}--filters{W} "Name=tag:Name,Values=MyInstance"')

Color.pl('\n {BO}Terminate your instance{W}\n')

Color.pl(' [root@aws]$ aws {C}ec2{W} terminate-instances {C}--instance-ids{W} i-5203422c')

Color.pl('\n [root@aws]$ {R}aws{W} {C}ec2{W} run-instances \\\n \
    {P}--image-id{W} ami-085925f297f89fce1 \\\n \
    {P}--count{W} 1  \\\n \
    {P}--instance-type{W} t2.micro \\\n \
    {P}--key-name{W} default \\\n \
    {P}--security-group-ids{W} sg-0efcc8890fd19836f \\\n \
    {P}--subnet-id{W} subnet-cf6496a9 \\\n \
    {P}--associate-public-ip-address{W}')

Color.pl('\n\t{BR}OR{W}\n')

Color.pl(' [root@aws]$ aws {C}ec2{W} run-instances {P}--image-id{W} ami-085925f297f89fce1 {P}--instance-type{W} t2.micro {P}--key-name{W} default {P}--security-group-ids{W} sg-0efcc8890fd19836f {P}--subnet-id{W} subnet-cf6496a9 {P}--associate-public-ip-address{W}\n')


'''
[--monitoring <value>] true|false
[--security-groups <value>] "string" "string"
[--user-data <value>]
[--private-ip-address <value>]
--associate-public-ip-address
'''

