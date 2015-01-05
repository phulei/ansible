require 'spec_helper'

describe command('which mvn') do
    it { should return_stdout '/opt/apache-maven-3.0.5/bin/mvn' }
end

describe file('/opt/apache-maven-3.0.5') do
    it { should be_directory }
end
