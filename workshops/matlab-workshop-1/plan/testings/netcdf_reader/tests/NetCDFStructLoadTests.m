classdef NetCDFStructLoadTests < matlab.unittest.TestCase

    properties
        NetCDFObj
        Filename = "C:\Users\delgr\Desktop\steinmetz_2017-01-08_Muller.nc"
    end

    methods (TestMethodSetup)
        % Setup for each test
        function createNetCDFObject(testCase)
            testCase.NetCDFObj = netcdf.NetCDF(testCase.Filename);
        end
    end

    methods (Test)
        % Test methods

        function structIsLoaded(testCase)
            dset = testCase.NetCDFObj.read2struct();
            testCase.verifyClass(dset, 'struct');
        end

        function CorrectVarsAreLoaded(testCase)
            dset = testCase.NetCDFObj.read2struct({'contrast_right', 'contrast_left'});
            testCase.assertTrue(ismember({'contrast_right'}, fieldnames(dset)));
            testCase.assertTrue(ismember({'contrast_left'}, fieldnames(dset)));
        end

        function DimensionsAreLoaded(testCase)
            dset = testCase.NetCDFObj.read2struct({'contrast_right'});
            testCase.assertTrue(ismember({'trial'}, fieldnames(dset)));
        end

        function DimensionsAreLoaded2(testCase)
            dset = testCase.NetCDFObj.read2struct({'pupil_x'});
            testCase.assertTrue(ismember({'trial'}, fieldnames(dset)));
            testCase.assertTrue(ismember({'time'}, fieldnames(dset)));
        end        


    end

end
