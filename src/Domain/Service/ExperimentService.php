<?php

namespace Genre\Domain\Service;

class ExperimentService
{
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
        $jsonParams = \json_encode($params);
        $jsonParams = str_replace('"', '\"', $jsonParams);
        $command = "echo 12345 | su - root -s /bin/bash -c 'python3 /var/www/genre/python/main.py experiment $jsonParams'";
        $output = null;
        $status = null;
        exec($command, $output, $status);

        $musicMetricsArray = json_decode($output[0], true);
        return [];
    }
}
