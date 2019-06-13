import unittest
from unittest import TestCase
from logger.experiment import Experiment
import pandas as pd

class TestExperiment(TestCase):

    def test__init_no_old_exp_no_logged_exp(self):
        """
        Test init when no old or logged experiments given
        :return: Expected to have a warning, and the internal df is empty
        :rtype:
        """
        with self.assertWarns(UserWarning):
            experiment = Experiment()
            self.assertTrue(experiment.df.empty)

    def test__init_from_csv(self):
        """
        Test init with old experiments in a csv
        :return:
        :rtype: Expected to have the internal df having the same data in the csv
        """
        experiment = Experiment(csv_file='results_old.csv')

        old_df = pd.read_csv('results_old.csv')

        assert old_df.equals(experiment.df)

    def test__init_from_yaml(self):
        """
        Test init with old experiment from csv and logged one from yaml
        :return: Expected to have internal df with the csv + yaml data
        :rtype:
        """
        # TODO: when yaml is supported
        '''
        experiment = Experiment(csv_file='results_old.csv')

        old_df = pd.read_csv('results_old.csv')

        assert old_df.equals(experiment.df)
        '''
        self.fail()


    def test__init_old_exp_incomplete_exp(self):
        """
        Test init with old csv experiment + logged experiment with missing info
        :return: Expected to have user warning + internal df is empty
        :rtype:
        """
        self.fail()

    def test__init_old_exp_complete_exp(self):
        """
        Test init with old csv experiment + logged experiment
        :return: Expected internal df = old csv + logged data
        :rtype:
        """
        self.fail()


    def test__init_no_old_exp_incomplete_exp(self):
        """
        Test init with no old experiment + logged experiment with missing info
        :return: Expected to have user warning + internal df is empty
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Experiment(config=exp_config)
            self.assertTrue(experiment.df.empty)

        with self.assertWarns(UserWarning):
            experiment = Experiment(meta_data=exp_meta)
            self.assertTrue(experiment.df.empty)

        with self.assertWarns(UserWarning):
            experiment = Experiment(results=exp_results)
            self.assertTrue(experiment.df.empty)

    def test__init_no_old_exp_complete_exp(self):
        """
        Test init with no old experiments and logged experiment
        :return: Expected internal df = logged data
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Experiment(meta_data=exp_meta, config=exp_config, results=exp_results)
            self.assertFalse(experiment.df.empty)

    def test_from_csv(self):
        """
        Test init with csv data, but no logged data
        :return: Expected to have internal df with csv data
        :rtype:
        """
        experiment = Experiment()
        experiment.from_csv(csv_file='results_old.csv')
        old_df = pd.read_csv('results_old.csv')

        self.assertFalse(experiment.df.empty)
        assert old_df.equals(experiment.df)

    def test_from_df(self):
        """
        Test init from a df
        :return: Expected internal df to have same data as passed df
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        experiment = Experiment()
        experiment.from_df(old_df)

        assert old_df.equals(experiment.df)

    def test_log_experiment(self):
        """
        Test logging extra experiment(s) data
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Experiment(csv_file='results_old.csv')
        experiment.log_experiment(meta_data=exp_meta, config=exp_config, results=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

    def test_log_experiment_no_previous_exp(self):
        """
        Test logging extra experiment(s) data with no previous records
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Experiment()
            experiment.log_experiment(meta_data=exp_meta, config=exp_config, results=exp_results, yaml_file=None)
            self.assertFalse(experiment.df.empty)
            #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
            exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)

            self.assertTrue(exp_df.equals(experiment.df))

        # Log another one
        experiment.log_experiment(meta_data=exp_meta, config=exp_config, results=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([exp_df, exp_df], axis=0, ignore_index=True, sort=False)

        self.assertTrue(exp_df.equals(experiment.df))

    def test_log_experiment_yaml(self):
        """
        Test logging extra experiment(s) data from yaml
        :return: Expected to have internal df appending logged data every time
        :rtype:
        """
        self.fail()


    def test_log_experiment_incomplete_attribs(self):
        """
        Test logging incomplete experiment data
        :return: Expected assertion
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()

        with self.assertRaises(AssertionError):
            experiment = Experiment()
            experiment.log_experiment(exp_meta, None, None, None)

    def test_log_experiment_bad_data_type(self):
        """
        Test passing non-dict type
        :return: Expected assertion
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = []
        exp_config = []
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertRaises(AssertionError):
            experiment = Experiment()
            experiment.log_experiment(exp_meta, exp_config, exp_results, None)


    def test_exp_to_df(self):
        """
        Test conversion from experiment attribs to one df
        :return: Expected merged df of meta, config and results
        :rtype:
        """
        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()

        with self.assertWarns(UserWarning):
            experiment = Experiment()
            df = experiment.exp_to_df(meta_data=exp_meta, config=exp_config, results=exp_results, yaml_file=None)
            self.assertFalse(df.empty)

            exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)

            self.assertTrue(exp_df.equals(df))

    def test_to_csv(self):
        """
        Test writing the full experiment df (including old one)
        :return:
        :rtype:
        """
        experiment = Experiment(csv_file='results.csv')
        experiment.to_csv('results.csv')
        df = pd.read_csv('results.csv')
        self.assertTrue(df.equals(experiment.df))

    def test_new_logged_exp_to_csv(self):
        """
        Test writing the full experiment df (including old one)
        :return:
        :rtype:
        """
        experiment = Experiment(csv_file='results.csv')
        experiment.to_csv('results.csv')
        df = pd.read_csv('results.csv')




        old_df = pd.read_csv('results_old.csv')
        meta_df, config_df, results_df = self.df_to_exp_attribs(old_df)
        exp_meta = meta_df.iloc[-1].to_dict()
        exp_config = config_df.iloc[-1].to_dict()
        exp_results = results_df.iloc[-1].to_dict()


        experiment = Experiment(csv_file='results_old.csv')
        experiment.log_experiment(meta_data=exp_meta, config=exp_config, results=exp_results, yaml_file=None)
        self.assertFalse(experiment.df.empty)
        #exp_df = old_df.iloc[-1]#pd.concat([meta_df.iloc[-1], config_df.iloc[-1], exp_results], axis=1)
        exp_df = pd.concat([pd.DataFrame([exp_meta]), pd.DataFrame([exp_config]), pd.DataFrame([exp_results])], axis=1)
        df = pd.concat([old_df, exp_df], axis=0, ignore_index=True, sort=False)
        self.assertTrue(df.equals(experiment.df))

        experiment.to_csv('results.csv')
        df = pd.read_csv('results.csv')
        self.assertTrue(df.equals(experiment.df))

    def test_from_yaml(self):
        """
        Test Convert yaml file into df
        :return: Expected returned df to be the same as in yaml file
        :rtype: DataFrame
        """
        self.fail()

    def test_to_yaml(self):
        """
        Test writing of yaml file from an experiment data frame
        :return: Expected to write yaml file with the same params in the experiment df's
        :rtype: yaml file written on desk
        """
        self.fail()

    # Utils
    def df_to_exp_attribs(self, df):
        """
        Segment the flat experiment df into: meta_data, config and results
        :param df: flat experiment df
        :type df: DataFrame
        :return: split meta_df, config_df, results_df
        :rtype: DataFrame, DataFrame, DataFrame
        """
        meta_cols = ['Name', 'Purpose', 'Description', 'Run file', 'Commit']
        config_cols = ['Features', 'Train_test_split', 'Size', 'maxlen', 'batch_size', 'epochs', 'type',
                       'lr', 'lstm_output_size', 'dense', 'dropout', 'embedding_size',
                       'pool_size', 'filters', 'kernel_size']
        results_cols = ['AUC', 'Val acc', 'Model file', 'Comment']
        meta_df = df[meta_cols]
        config_df = df[config_cols]
        results_df = df[results_cols]

        return meta_df, config_df, results_df

if __name__ == '__main__':
    unittest.main()
