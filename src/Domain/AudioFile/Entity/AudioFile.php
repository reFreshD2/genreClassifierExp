<?php

namespace Genre\Domain\AudioFile\Entity;

use Genre\Domain\MusicMetrics\Entity\MusicMetrics;
use Doctrine\ORM\Mapping as ORM;
use Genre\Domain\AudioFile\Repository\AudioFileRepository;

/**
 * @ORM\Entity(repositoryClass=AudioFileRepository::class)
 */
class AudioFile
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $path;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $hash;

    /**
     * @ORM\OneToOne(targetEntity=MusicMetrics::class, inversedBy="audioFile", cascade={"remove"})
     */
    private $musicMetrics;

    public function __construct(string $path, string $hash)
    {
        $this->hash = $hash;
        $this->path = $path;
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getPath(): ?string
    {
        return $this->path;
    }

    public function setPath(string $path): self
    {
        $this->path = $path;

        return $this;
    }

    public function getHash(): ?string
    {
        return $this->hash;
    }

    public function setHash(string $hash): self
    {
        $this->hash = $hash;

        return $this;
    }

    public function getMusicMetrics(): ?MusicMetrics
    {
        return $this->musicMetrics;
    }

    public function setMusicMetrics(MusicMetrics $musicMetrics): void
    {
        $this->musicMetrics = $musicMetrics;
    }
}
