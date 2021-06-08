<?php

namespace Genre\Domain\MusicMetrics\Entity;

use Genre\Domain\MusicMetrics\Repository\MusicMetricsRepository;
use Doctrine\ORM\Mapping as ORM;
use Genre\Domain\AudioFile\Entity\AudioFile;

/**
 * @ORM\Entity(repositoryClass=MusicMetricsRepository::class)
 */
class MusicMetrics
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="float")
     */
    private $minFreq;

    /**
     * @ORM\Column(type="float")
     */
    private $maxFreq;

    /**
     * @ORM\Column(type="float")
     */
    private $avgFreq;

    /**
     * @ORM\Column(type="float")
     */
    private $minAmp;

    /**
     * @ORM\Column(type="float")
     */
    private $maxAmp;

    /**
     * @ORM\Column(type="float")
     */
    private $avgAmp;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $rhythm;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $rate;

    /**
     * @ORM\Column(type="json")
     */
    private $instrumentsSoundsCharacter = [];

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $musicForm;

    /**
     * @ORM\Column(type="float")
     */
    private $spectralCentroid;

    /**
     * @ORM\Column(type="float")
     */
    private $spectralRollOf;

    /**
     * @ORM\Column(type="float")
     */
    private $spectralBandWidth;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     *
     */
    private $genre;

    /**
     * @ORM\OneToOne(targetEntity=AudioFile::class, mappedBy="musicMetrics", cascade={"remove"})
     */
    private $audioFile;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getMinFreq(): ?float
    {
        return $this->minFreq;
    }

    public function setMinFreq(float $minFreq): self
    {
        $this->minFreq = $minFreq;

        return $this;
    }

    public function getMaxFreq(): ?float
    {
        return $this->maxFreq;
    }

    public function setMaxFreq(float $maxFreq): self
    {
        $this->maxFreq = $maxFreq;

        return $this;
    }

    public function getAvgFreq(): ?float
    {
        return $this->avgFreq;
    }

    public function setAvgFreq(float $avgFreq): self
    {
        $this->avgFreq = $avgFreq;

        return $this;
    }

    public function getMinAmp(): ?float
    {
        return $this->minAmp;
    }

    public function setMinAmp(float $minAmp): self
    {
        $this->minAmp = $minAmp;

        return $this;
    }

    public function getMaxAmp(): ?float
    {
        return $this->maxAmp;
    }

    public function setMaxAmp(float $maxAmp): self
    {
        $this->maxAmp = $maxAmp;

        return $this;
    }

    public function getAvgAmp(): ?float
    {
        return $this->avgAmp;
    }

    public function setAvgAmp(float $avgAmp): self
    {
        $this->avgAmp = $avgAmp;

        return $this;
    }

    public function getRhythm(): ?string
    {
        return $this->rhythm;
    }

    public function setRhythm(string $rhythm): self
    {
        $this->rhythm = $rhythm;

        return $this;
    }

    public function getRate(): ?string
    {
        return $this->rate;
    }

    public function setRate(string $rate): self
    {
        $this->rate = $rate;

        return $this;
    }

    public function getInstrumentsSoundsCharacter(): string
    {
        return implode(',' ,$this->instrumentsSoundsCharacter);
    }

    public function setInstrumentsSoundsCharacter(array $instrumentsSoundsCharacter): self
    {
        $this->instrumentsSoundsCharacter = $instrumentsSoundsCharacter;

        return $this;
    }

    public function getMusicForm(): ?string
    {
        return $this->musicForm;
    }

    public function setMusicForm(string $musicForm): self
    {
        $this->musicForm = $musicForm;

        return $this;
    }

    public function getSpectralCentroid(): ?float
    {
        return $this->spectralCentroid;
    }

    public function setSpectralCentroid(float $spectralCentroid): self
    {
        $this->spectralCentroid = $spectralCentroid;

        return $this;
    }

    public function getSpectralRollOf(): ?float
    {
        return $this->spectralRollOf;
    }

    public function setSpectralRollOf(float $spectralRollOf): self
    {
        $this->spectralRollOf = $spectralRollOf;

        return $this;
    }

    public function getSpectralBandWidth(): ?float
    {
        return $this->spectralBandWidth;
    }

    public function setSpectralBandWidth(float $spectralBandWidth): self
    {
        $this->spectralBandWidth = $spectralBandWidth;

        return $this;
    }

    public function getGenre(): ?string
    {
        return $this->genre;
    }

    public function setGenre(string $genre): self
    {
        $this->genre = $genre;

        return $this;
    }

    public function getAudioFile(): ?AudioFile
    {
        return $this->audioFile;
    }

    public function setAudioFile(AudioFile $audioFile): void
    {
        $this->audioFile = $audioFile;
    }

    public static function createFromArray(array $array): MusicMetrics {
        $musicMetrics = new self();

        $musicMetrics->setMinFreq($array['_MusicMetrics__minFreq'] ?? 0);
        $musicMetrics->setAvgFreq($array['_MusicMetrics__avgFreq'] ?? 0);
        $musicMetrics->setMaxFreq($array['_MusicMetrics__maxFreq'] ?? 0);
        $musicMetrics->setMinAmp($array['_MusicMetrics__minAmp'] ?? 0);
        $musicMetrics->setMaxAmp($array['_MusicMetrics__maxAmp'] ?? 0);
        $musicMetrics->setAvgAmp($array['_MusicMetrics__avgAmp'] ?? 0);
        $musicMetrics->setRhythm($array['_MusicMetrics__rhythm'] ?? 'Неопределенный');
        $musicMetrics->setRate($array['_MusicMetrics__rate'] ?? 'Неопределенный');
        $musicMetrics->setInstrumentsSoundsCharacter($array['_MusicMetrics__instrumentsSoundsCharacter']);
        $musicMetrics->setMusicForm($array['_MusicMetrics__musicForm'] ?? 'A');
        $musicMetrics->setSpectralCentroid($array['_MusicMetrics__spectralCentroid'] ?? 0);
        $musicMetrics->setSpectralRollOf($array['_MusicMetrics__spectralRollOf'] ?? 0);
        $musicMetrics->setSpectralBandWidth($array['_MusicMetrics__spectralBandWidth'] ?? 0);

        return $musicMetrics;
    }
}
