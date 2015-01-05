require 'spec_helper'

describe package('jdk') do 
  it { should be_installed }
end

describe command('which java') do
  it { should return_stdout '/usr/bin/java' }
end
