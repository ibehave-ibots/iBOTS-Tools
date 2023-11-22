classdef NetCDFTableLoadTests < matlab.unittest.TestCase

    properties
        NetCDFObj
        Filename = "C:\Users\delgr\Desktop\steinmetz_2017-01-08_Muller.nc"
    end

    methods (TestMethodSetup)
        % Setup for each test
        function createNetCDFObject(testCase)
            testCase.NetCDFObj = netcdf.Reader(testCase.Filename);
        end
    end

    methods (TestClassSetup)
        % Shared setup for the entire test class
    end


    methods (Test)
        % Test methods

        function tableIsCreated(testCase)
            t = testCase.NetCDFObj.read2table({'contrast_left', 'contrast_right'});
            testCase.assertClass(t, 'table');
        end

        function WorksWithStringArray(testCase)
            t = testCase.NetCDFObj.read2table("contrast_left");
            testCase.assertClass(t, 'table');
            columnNames = t.Properties.VariableNames;
            testCase.assertTrue(ismember('contrast_left', columnNames));
        end

        function WorksWithCellArrayOfStrings(testCase)
            t = testCase.NetCDFObj.read2table({"contrast_left"});
            testCase.assertClass(t, 'table');
            columnNames = t.Properties.VariableNames;
            testCase.assertTrue(ismember('contrast_left', columnNames));
        end

        function tableIncludesRequestedFields(testCase)
            t = testCase.NetCDFObj.read2table({'contrast_left', 'contrast_right', 'pupil_x'});
            columnNames = t.Properties.VariableNames;
            testCase.assertTrue(ismember('contrast_left', columnNames));
            testCase.assertTrue(ismember('contrast_right', columnNames));
            testCase.assertTrue(ismember('pupil_x', columnNames));
        end

        function tableIncludesAssociatedDimensions(testCase)
            t = testCase.NetCDFObj.read2table({'contrast_left', 'contrast_right', 'pupil_x'});
            columnNames = t.Properties.VariableNames;
            testCase.assertTrue(ismember('time', columnNames));
            testCase.assertTrue(ismember('trial', columnNames));
        end

        function EachColumnIs1D(testCase)
            t = testCase.NetCDFObj.read2table({'contrast_left', 'contrast_right', 'pupil_x', 'pupil_y'});
            for col = t
                testCase.verifySize(col, [height(t), 1]);
            end
        end

        function TableIsUnstacked(testCase)
            t = testCase.NetCDFObj.read2table({'contrast_left', 'contrast_right', 'pupil_x', 'pupil_y'});
            pupil_x = ncread(testCase.Filename, "pupil_x");
            testCase.verifySize(t.pupil_x, [numel(pupil_x), 1])
        end
    end

end