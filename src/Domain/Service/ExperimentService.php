<?php

namespace Genre\Domain\Service;

class ExperimentService
{
    private const PYTHON_PATH = '/var/www/genre/python/';

    public function getExperimentResult(array $params): array
    {
        $params = array_filter($params);
        if (isset($params['random'])) {
            unset($params['random']);
            $params['type'] = 'random';
        } else {
            unset($params['equable']);
            $params['type'] = 'equable';
        }

        $file = new \SplFileObject(self::PYTHON_PATH . 'params.json', "w");
        $file->fwrite(\json_encode($params));

        $command = "echo 12345 | su - root -s /bin/bash -c 'python3 "
            . self::PYTHON_PATH
            . "main.py experiment "
            . $file->getRealPath()
            . "'";
        $output = null;
        $status = null;
        exec($command, $output, $status);

        if ($status !== 0) {
            return [];
        }

        $result = json_decode($output[0], true);
        $result['quality']['Средние значения'] = [
            'Точность' => $result['quality']['Средняя точность'],
            'Полнота' => $result['quality']['Средняя полнота'],
        ];
        $result['Fscore'] = $result['quality']['F-мера'];
        unset(
            $result['quality']['Средняя точность'],
            $result['quality']['Средняя полнота'],
            $result['quality']['F-мера']
        );

        return $result;
    }
}
