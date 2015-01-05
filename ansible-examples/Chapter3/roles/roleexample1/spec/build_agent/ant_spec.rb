require 'spec_helper'

describe command('which ant') do
    it  { should return_stdout '/opt/apache-ant-1.7.1/bin/ant' }
end

describe file('/opt/apache-ant-1.7.1') do
    it { should be_directory }
end
