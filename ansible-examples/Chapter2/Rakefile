require 'rubygems'
require 'bundler/setup'
require 'rake'
require 'rspec/core/rake_task'
#require 'json'
hosts = [
  {
    :name  => 'host1',
    :ip    => '192.168.33.10',
    :playbook => %w( example1 ),
  },
]

desc "Run serverspec on all hosts"
task :serverspec => 'serverspec:all'

namespace :serverspec do
  #If you have a lot of hosts and want to run it in parallel
  #multitask :all => hosts.map {|h| 'serverspec:' + h[:name] }
  task :all => hosts.map {|h| 'serverspec:' + h[:name] }
  hosts.each do |host|
    desc "Run serverspec to #{host[:name]}"
    RSpec::Core::RakeTask.new(host[:name].to_sym) do |t|
      ENV['TARGET_HOST'] = host[:ip]
      puts "-------------------------------------"
      puts "Running #{host[:playbook]} serverspec tests on - #{host[:name]} "
      t.pattern = "spec/#{host[:playbook]}/*_spec.rb"
      puts "hostname/ip - #{host[:name]}"
    end
  end
end
