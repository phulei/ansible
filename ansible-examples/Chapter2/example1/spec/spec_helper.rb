#!/usr/bin/env ruby
require 'rubygems'
require 'serverspec'
require 'pathname'
require 'net/ssh'
#require 'json'

include Serverspec::Helper::Ssh
include Serverspec::Helper::DetectOS

RSpec.configure do |c|
  c.host  = ENV['TARGET_HOST']
  puts "C HOST --- #{c.host}"
  options = Net::SSH::Config.for(c.host)
  #can have all possible keys if you're using keys
  options[:keys] = ["~/.ssh/ansible_key"]
  options[:paranoid] = false
  user    = 'vagrant'
  c.ssh   = Net::SSH.start(c.host, user, options)
  c.os    = backend.check_os
end
